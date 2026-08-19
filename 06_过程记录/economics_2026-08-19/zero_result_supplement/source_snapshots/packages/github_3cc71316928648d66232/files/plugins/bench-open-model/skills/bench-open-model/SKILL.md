---
name: bench-open-model
description: Benchmark any open-weight vLLM-servable Hugging Face model on AWS GPU hardware. Sizes the model's VRAM needs, picks the right EC2 GPU instance type and region, provisions it, serves the model on vLLM, runs a cache-honest concurrency sweep, writes a report, and tears everything down. Use when asked to benchmark / test / evaluate the throughput, latency, or serving capacity of an open-weight model on AWS, pick a GPU instance type for a model, size VRAM for a model, or measure tokens-per-second or requests-per-day. Covers text LLMs and multimodal / vision / OCR models.
---

# Benchmark an open-weight model on AWS

Takes a Hugging Face model ID and produces a defensible throughput number on real GPU
hardware, then cleans up. Works for any model vLLM can serve - text LLMs, MoE models, and
multimodal (vision / document) models. The sizing and provisioning path is common to all;
only the load-generation step branches on modality.

## WARNING: this spends real money and is not for production accounts

Read this to the user before phase 3, and do not proceed without their explicit go-ahead.

- **This plugin launches EC2 GPU instances, which cost roughly $2-15/hr and in some cases
  over $100/hr.** Charges begin at launch and continue until the instance is terminated,
  whether or not anyone is watching. A forgotten instance is the main risk here.
- **Never run this against a production account or environment.** Use a dedicated sandbox,
  development, or test account. Each run creates a CloudFormation stack owning an EC2
  instance, a security group, a key pair, and an IAM role, and teardown deletes that stack.
  The orphan sweep only offers stacks tagged `Purpose=vllm-benchmark` that the current
  identity created, and requires confirmation, but it is still a delete operation.
- **This is a load-generation tool.** Point it only at an endpoint it provisioned itself.
  Never aim the benchmark at a shared, staging, or production inference endpoint: it will
  saturate it on purpose.
- **Teardown is mandatory, not optional.** Run it even if the benchmark fails or the session
  is interrupted, and run it BEFORE writing the report. Then confirm to the user that spend
  has stopped. If `teardown.sh` exits nonzero, resources may still be billing.
- Requires real AWS credentials with permission to launch instances. Confirm which account
  and region you are operating in before phase 3, and say it out loud in the plan.

**The hard part is not running a load test - it is running one whose numbers are true.**
Inference servers cache aggressively, and a contaminated run reports a plausible number that
can be wrong by a factor of 3 or more. The guardrails in these scripts each exist because a
real run produced wrong numbers without them. Do not route around them;
`${CLAUDE_PLUGIN_ROOT}/references/lessons.md` documents what each one catches.

## Workflow

Phases 1-2 are cheap and read-only. Phase 3 onward spends money. Get explicit
confirmation once, at the end of phase 2, then run 3-7 unattended.

### 1. Size the model, pick the hardware

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/size_model.py <hf-model-id> \
  --max-model-len 32768 --concurrency 32 --regions us-east-1,us-west-2,eu-central-1
```

Prints params, weight/KV/overhead VRAM budget, and ranked candidate instances with live
On-Demand pricing and offered AZs. Everything is queried live - no hardcoded instance
tables, so new GPU families appear on their own.

Read the output, then choose deliberately:

- **Prefer the smallest single-GPU box that fits** (`TP` column = 1). One replica per GPU
  beats tensor-parallel for models that fit on one card - see `references/lessons.md` section 4.
- **Set `--max-model-len` and `--concurrency` to what you will actually serve.** They
  multiply into the KV-cache term, which frequently dwarfs the weights and is what really
  picks the hardware. Defaults of 32768 x 32 can push an 8B model onto a $100+/hr box; the
  same model at 8k x 8 fits a ~$2/hr card. The script warns when KV exceeds 2x weights.
- If nothing fits, lower `--max-model-len` or try a quantized checkpoint before upsizing.
- If the user named a specific instance family (a common request - they are often
  evaluating that hardware, not shopping for the cheapest), use it and skip the ranking.
- Gated model -> `HF_TOKEN` must be exported; the script says so if it hits a 401/403.
- **The script may REFUSE to size a model, by design.** Its KV-cache model covers standard
  full attention (MHA/GQA/MQA). It fails closed on MLA (DeepSeek-V2/V3), active
  sliding-window, hybrid stacks (Qwen3-Next, Jamba) and Mamba/SSM, because a plausible wrong
  number would pick the wrong instance. When that happens: **do not pass
  `--force-kv-estimate` and proceed as if the number were real.** Instead pick an instance
  with generous VRAM headroom, provision, and read the actual `GPU KV cache size` line from
  the vLLM startup log plus `nvidia-smi`. Report the measured figure. Provisioning, serving
  and the benchmark are architecture-agnostic, so everything after sizing works normally.

Confirm the vLLM image supports the architecture before provisioning. Check the model's
`architectures` field against vLLM's supported list; if it is newly added, note which vLLM
version introduced it and pin at least that version via `--vllm-image`.

### 2. Present the plan and get a go-ahead

Show the user, concretely, and get one explicit go-ahead before spending anything:

- **Which AWS account and region** you are about to launch in. Run
  `aws sts get-caller-identity` and show it. If it looks like a production account, stop and
  ask; do not proceed on assumption.
- Model + params, instance type, `$/hr`, and estimated total for the run.
- What will be measured, and at what input shape.
- That teardown is automatic, and what it will delete.

Then proceed without further prompting.

Estimate honestly: model download + load is typically 5-15 min, the sweep 10-30 min. A
~$3/hr instance for a ~1 hr session is ~$3, but say so rather than letting them guess. If the
recommended instance is expensive, say the hourly rate plainly rather than burying it.

### 3. Provision

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/provision.sh \
  --model <hf-model-id> --instance-type <type> --region <region> \
  --max-model-len 32768 --tp 1 \
  --fallback-regions us-west-2,eu-central-1 \
  --extra-flags "--chat-template-content-format string" \
  --vision \
  --yes
```

Pass `--vision` **only for vision/OCR models.** It installs the PDF rasterization stack
(`pypdfium2`, `pillow`, `ocrtestdata`) that phase 5 needs to generate page images. A text-LLM
benchmark does not need it and should omit the flag.

`--yes` acknowledges the cost. **Only pass it after the user has approved the plan in phase
2.** Without it the script prints the account, region and cost, then refuses to launch when
there is no TTY, which is deliberate: an expensive launch must never be the silent default.

**Everything is one CloudFormation stack**: key pair, security group, IAM role, instance
profile, and the instance. That matters for teardown - a single `delete-stack` removes them
all in the correct dependency order, rather than the script sequencing deletions by hand.
Each run gets a unique id, so launching the same model twice creates two independent stacks
instead of the second clobbering the first.

Tries every offered AZ in the region, then each fallback region. A capacity failure rolls the
stack back and deletes it, so a failed attempt leaves nothing billing.

Writes `.bench-state/<run-id>.json` **before** calling `create-stack`, so teardown is possible
even if the session dies mid-launch. **If you are resuming a lost session, look for state
files first** - `ls .bench-state/*.json` - and if there are none, run
`teardown.sh --sweep-region <region>` to find orphaned stacks.

Security posture this sets up, worth stating in the report: SSH from your IP only (port 8000
is **not** opened), IMDSv2 required, EBS encrypted, and the private key generated into SSM
rather than written by you.

`--extra-flags` notes: some document VLMs need `--chat-template-content-format string`.

`--trust-remote-code` is **off by default** and must be passed explicitly. It lets the model
repository execute its own Python on the instance, so only pass it for a repo you trust, and
say so in the report when you do.

`--max-lifetime-hours` (default 8) arms an on-instance watchdog that self-terminates as a
backstop. It is not a substitute for teardown; it is insurance against a lost session. The
instance role carries a tag-scoped `ec2:TerminateInstances` so the watchdog can genuinely
terminate rather than merely stop.

If `HF_TOKEN` is set, it is stored as an SSM SecureString and **the instance deletes that
parameter as soon as it has read the value**, so the credential is at rest in the account for
seconds rather than for the life of the run.

### 4. Wait for the model to load

```bash
ssh -o StrictHostKeyChecking=accept-new -i <keyfile> ubuntu@<ip> \
  'cat /opt/vllm-status 2>/dev/null || tail -5 /var/log/user-data.log'
```

`READY` = serving. `TIMEOUT` = it failed; read `/var/log/user-data.log` and
`docker logs vllm`. Poll every ~30s. Do not start benchmarking before `READY`.

Common failures: unsupported architecture for the vLLM version (pin a newer image);
OOM at load (lower `--max-model-len` or `--gpu-util`); gated repo (missing `HF_TOKEN`).

### 5. Copy the harness up (and generate inputs, for vision models)

```bash
scp -i <keyfile> ${CLAUDE_PLUGIN_ROOT}/scripts/{gen_pages.py,bench.py} ubuntu@<ip>:/tmp/
```

**Text models need nothing further** - `bench.py` synthesizes unique prompts itself.

**Before you sweep, agree the input shape with the user.** This is what makes the number
mean something, and the defaults are almost certainly not their workload:

- **Text:** `--prompt-tokens` and `--max-tokens`. Input length drives prefill cost; the
  output cap bounds the result. A summarization workload (long in, short out) and a chat
  workload (short in, long out) saturate differently - see `references/lessons.md` section 2.
- **Vision:** input resolution, via `--dpi`. Generate the inputs, more than the sweep will
  consume:

```bash
ssh -i <keyfile> ubuntu@<ip> 'python3 /tmp/gen_pages.py --pages 300 --dpi 300 --out /tmp/pages'
```

  Resolution is the dominant lever - vision tokens scale with pixel count, so halving DPI
  roughly quarters the prefill work. **Ask what the real inputs look like, or state the
  assumption prominently in the report.** `gen_pages.py` (vision only; needs `--vision` at provision time) refuses to emit duplicate pages and
  warns if it cannot make enough.

### 6. Run the sweep

**Restart the container first so the cache is cold.** This is not optional.

```bash
ssh -i <keyfile> ubuntu@<ip> 'docker restart vllm && sleep 60'

# text:
ssh -i <keyfile> ubuntu@<ip> 'python3 /tmp/bench.py --mode text --prompt-tokens 4096 \
   --concurrency 1,8,16,32 --max-tokens 512'
# vision:
ssh -i <keyfile> ubuntu@<ip> 'python3 /tmp/bench.py --mode vision --pages /tmp/pages \
   --concurrency 1,8,16,32 --max-tokens 1024'
```

Runs on the box against `localhost`, so no WAN latency. Every request gets a unique payload;
the script aborts rather than reusing any.

Sweep **several** concurrency levels - a single point cannot show you where throughput stops
scaling, which is the number worth reporting.

**Then validate before you believe it:**

```bash
ssh -i <keyfile> ubuntu@<ip> "docker logs vllm 2>&1 | grep -iE 'cache hit rate' | tail -5"
```

Confirm ~**0%** prefix / multimodal cache hit rate. `bench.py` also self-checks: it **exits
nonzero and marks levels invalid** if any request failed, was truncated at `max_tokens`, or
returned an incomplete stream. A nonzero exit means do not report the numbers at all.

It warns when TTFT p50 *fell* as concurrency rose (the cache-contamination signature) and when
p99 was suppressed for too few samples. Sanity-check `avg_prompt_tokens` against the input
shape you intended; if it is far off, preprocessing is not doing what you think. In text mode,
pass `--tokenizer <hf-repo-id>` to have prompt lengths verified rather than estimated.

Where throughput goes flat is the saturation point - the real ceiling. Extra concurrency past
it only inflates latency.

### 7. Retrieve results, TEAR DOWN, then write the report

Do these in this order. Writing the report first means an instance bills for however long the
write takes, and if anything interrupts you the instance is still running.

**First** copy the raw results off the box:

```bash
scp -i <keyfile> ubuntu@<ip>:/tmp/bench_results.json ./
scp -i <keyfile> ubuntu@<ip>:/opt/vllm-runtime.txt ./     # exact image digest + vLLM version
```

**Then tear down immediately:**

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/teardown.sh --state .bench-state/<run-id>.json
```

One `delete-stack` removes the instance, security group, IAM role, instance profile, key pair
and the SSM parameter holding the private key, in dependency order. It then **independently
confirms** the stack is gone, deletes the token parameter, and checks nothing tagged with this
run id survives. If it cannot confirm deletion it **keeps the state file and exits nonzero** -
treat that as "still billing" and investigate, do not assume it worked.

Run it even if the benchmark failed. `--all` tears down every state file. `--sweep-region <r>`
lists orphaned stacks **you** own with their ages and instance ids, then requires confirmation
before deleting anything.

Report the teardown result to the user explicitly, then **write the report from the retrieved
files.** Include, at minimum: instance/GPU/region, model, the exact vLLM version and image
digest from `vllm-runtime.txt`, the input shape you benchmarked (prompt/output token lengths,
or resolution for vision), the sweep table (req/sec, per-day, tok/s, TTFT p50/p95/p99, E2E,
errors), the saturation point, `$/hr` and derived cost-per-1k-units, and **an explicit caveats
section**. State plainly what was *not* measured: accuracy is not measured by any of this,
synthetic inputs are more uniform than real traffic, and output token caps bound the result.
If `--trust-remote-code` was used, say so.

Report the teardown result to the user explicitly - they need to know spend has stopped.

## Rules

- **Never report a number you have not cache-validated.** Cold container, unique payloads,
  ~0% cache hit rate, TTFT rising with concurrency. All four, every time.
- **Always tear down, and do it BEFORE writing the report.** Even on failure, even on
  interruption. GPU instances are $2-15/hr. A nonzero exit from `teardown.sh` means resources
  may still be billing - investigate, never assume success.
- **Never report a run that exited nonzero.** `bench.py` fails the run when requests error or
  responses are truncated; those numbers describe a different workload than you asked for.
- **Never run against a production account.** Confirm the account and region in phase 2 and
  state them in the plan. Sandbox or dev accounts only.
- **Never point the benchmark at an endpoint this plugin did not provision.** It generates
  saturating load by design.
- **Never widen the security group to 0.0.0.0/0.** It is IP-locked by design.
- **Say what you did not measure.** These scripts measure throughput and latency only.
  Never let a throughput result be read as an accuracy result.
- Report the saturation point, not the peak concurrency you happened to test.
- **State the input shape alongside every number.** A throughput figure without the prompt
  and output lengths (or input resolution) it was measured at is not reproducible and not
  useful for capacity planning.

## Files

All paths are under `${CLAUDE_PLUGIN_ROOT}`, which resolves to this plugin's install
directory. Run the scripts from there - do not copy them into the project.

| File | Role | Runs on |
| :-- | :-- | :-- |
| `scripts/size_model.py` | HF metadata -> VRAM budget -> ranked instances (live pricing) | your machine |
| `scripts/stack.yaml` | CloudFormation template: key pair, SG, IAM role, instance | - |
| `scripts/provision.sh` | Creates the stack; unique run id, AZ/region fallback, state file | your machine |
| `scripts/teardown.sh` | Deletes the stack, verifies it is gone, owner-scoped orphan sweep | your machine |
| `scripts/user-data.sh.tmpl` | vLLM bootstrap, fail-fast, lifetime watchdog, health marker | the instance (via user-data) |
| `scripts/gen_pages.py` | Unique pages at a chosen DPI, duplicate-proof | the instance |
| `scripts/bench.py` | Concurrency sweep; rejects truncated/failed samples, fails nonzero | the instance |
| `references/lessons.md` | **Measured findings and the trap behind each guardrail** | - |

Read `references/lessons.md` before overriding a guardrail or explaining a surprising
result. Every guardrail in these scripts traces to a specific expensive mistake documented
there.

A `SessionStart` hook checks `.bench-state/` for instances left running by an earlier
session and surfaces them with a ready-to-run teardown command. If you see that warning,
tell the user before doing anything else - it means money is being spent right now.
