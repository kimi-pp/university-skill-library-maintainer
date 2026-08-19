---
name: help
description: Explain what archirules is, what problem it solves, what it costs and what it does not do. Use when somebody asks what this method is, whether it is worth adopting, or why a rule is worded the way it is.
---

# What archirules is

**`--help`** — if `$ARGUMENTS` is `--help`, run
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/help.py help`, show its output, and stop there.

## Usage

```
/archirules:help [--help]
```

Explains the method: the problem it addresses, what it actually consists of, what it costs, and
what it does not do.

**Needs from you:** nothing.

**Will not:** tell you it will make your project succeed. It addresses one specific failure and
is honest about the rest.

### Examples

```
/archirules:help          the whole explanation — problem, cost, limits, state of the evidence
/archirules:help --help   one screen instead: what it prints and what it will not claim
```

## The problem

A project rarely loses to a hard decision. It loses to decisions **made silently** — by the
order in which somebody touched files, by a default value nobody chose, by nobody writing down
the alternative that was rejected.

The symptoms are recognisable:

- somebody proposes an option that was already weighed and dropped, and nobody can say why it
  fell, so it gets re-argued from scratch;
- a document describes behaviour the code no longer has, and has been wrong for months;
- a phase is "done", and what that means is settled afterwards by whoever is arguing;
- a check has been green since it was written, and nobody has ever seen it red.

Six months later nobody can say whether something was a choice or an accident. That is the
failure this addresses. Not planning, not estimation, not quality in general.

## What it actually is

Files in `docs/architecture/`, versioned with the code and reviewed like code, plus rules about
what goes in them, plus checkers that fail when they rot.

Four of them are **registers**, and each answers a different question about how well something is
known:

| file | answers |
|---|---|
| `decisions/ADR-NNNN-*.md` | what was decided, what was rejected and why, at what cost |
| `open-questions.md` | what is not known yet, and what it holds up |
| the phase register | what is done, what is next, and how we will know it is finished |
| the verification register | what is **verified**, as opposed to **asserted** |

Alongside them: `README.md`, the index, which carries what binds **every** piece of work rather
than only its own area; and, where a choice needs weighing before it is made, an analysis file.

That set is closed on purpose. A new register has to be justified by a defect its absence caused
— not by symmetry with another methodology — because a register nobody's work depends on is the
first one to stop being maintained, and an unmaintained register is worse than none.

The first three registers are needed from day one. The verification register is started at the first
defect caused by an unverified claim, at which point its usefulness is not in question.

There is no meeting, no role, no board, no estimation ritual. The artefacts are files in the
repository.

## The four ideas that make it more than paperwork

**1. A decision records its costs, in the indicative.** Not "risks", not "to consider" — costs,
accepted. If you cannot name a single cost, the decision is not understood yet, and the answer
is to go back to analysis rather than write the record. A document listing only benefits is not
a decision; it is a justification written afterwards. When the cost lands, the only question
anybody asks is "did we know?", and that section is the answer.

**2. A doubt becomes a numbered question, not an on-the-spot call.** An unrecorded question gets
settled by the order in which somebody touches files. That is a resolution — just one nobody
made, that nobody can find, and that nobody agreed to.

**3. A phase's acceptance criterion is written before the work.** Not "do persistence" but "an
instance survives a restart and resumes". A criterion written afterwards is always met, which is
why writing it first is the whole mechanism.

**4. A gate is not finished until it has been shown to fail.** Break it deliberately, watch it
go red, revert. **A check that cannot fail looks exactly like a check that passes** — the same
green, the same silence, and no way to tell them apart by reading.

## Why the rules read the way they do

There are seven rules of conduct and ten of execution, and **every one exists because its
absence broke something specific**. The incidents are kept apart from the rules, in
`CASEBOOK.md`, so a rule stays readable without knowing somebody else's project. A few, so the
claim is checkable rather than atmospheric:

- **C-01** — a gate that could not fail. It reported success against deliberately broken input,
  for four successive versions.
- **C-06** — changing one punctuation mark switched off thirty-seven checks. The run stayed
  green; the count silently went to zero.
- **C-11** — a check with no self-test case of its own turned out to be incapable of firing at
  all, under any input, in either language. A fully green self-test said nothing about it.

That is also the answer to "is this just somebody's opinion". It is a list of failures and the
rule each one produced. Where there is no incident behind a rule, there is no rule.

## What is mechanised, and what is not

Three checkers, each shipping the proof that it can fail:

| script | axis |
|---|---|
| `conform.py` | structure inside one file: required sections, numbering, shape |
| `consistency.py` | agreement **between** registers, which no single file reveals |
| `trace.py` | register entries against the commits that implement them |

`selftest.sh` and `selftest-consistency.sh` are not development aids. They break a known-good
set in each way the checker claims to catch and require it to notice. Run them before trusting a
result.

**Not mechanised, and said out loud rather than implied:**

- whether a cost that was written down is **true** — the checker verifies the section exists,
  not that its contents are honest;
- whether the prose can be understood by somebody who was not there. No mechanical check for
  this is known, and a weak one would be worse than none, because it would create the impression
  that the question is covered;
- whether a decision is any good. The method makes it visible, dated, and accompanied by the
  alternative that was rejected. That is all.

The line between the two is deliberate: a rule that can be checked mechanically should be, and a
rule that cannot should be recorded **explicitly as a convention** with the warning sign by which
it is recognised. A rule that pretends to be enforced and is not is worse than an explicit
convention, because nobody watches it and everybody assumes somebody else does.

## What it costs

- **Every decision costs a document**, including the ones that turn out not to matter. There is
  no reliable way to know in advance which those are.
- **The registers can go stale**, and an unmaintained register is worse than none, because it
  looks current. This is why one rule is about correcting a record inside the record rather than
  deleting the sentence quietly, and why there is an audit skill at all.
- **It slows the first version down.** Naming a cost and a rejected alternative takes longer
  than deciding. It pays back at the point somebody asks why, which may be never on a project
  that ends in three months.
- **The checkers are code in your repository**, with the maintenance that implies.

## What it does not do

- **It does not replace code review.** The registers govern decisions, not implementations.
- **It does not survive neglect.** See above; this is the main way it fails.
- **It does not carry mechanical gates between projects.** Concrete checks belong to a
  repository. What travels is the pattern and the checklist.
- **It does not prevent a bad decision.** It makes one visible, dated, and accompanied by the
  alternative that was rejected.

## The honest state of the evidence

This method has been applied end to end to **one** project: the repository that carries it. That
is not nothing — a plugin whose author does not apply it to their own work is an argument
against itself — but it is also not a track record.

The phase register keeps a hard gate for exactly this, and it is not yet passed: *somebody who
did not co-create the method uses it without asking its author how*. Until that happens, this is
a private working habit with documentation, and the register says so in those words rather than
waiting to be asked.

## Where to start

```
/archirules:bootstrap
```

Creates the registers in a project that has none, in the language you choose. Then, in the order
you will actually meet them: `/archirules:oq` when you hit a doubt, `/archirules:adr` when
something is decided, `/archirules:phases` before starting a block of work,
`/archirules:verification` before trusting any check, `/archirules:audit` periodically.

`--help` on any of them says what it needs from you and what it will not do.
