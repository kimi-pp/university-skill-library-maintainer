# CS Thesis Reviewer Skill

`cs-thesis-reviewer` is a standalone agent skill for reviewing, planning, and revising computer science master's theses.

It helps an agent check thesis structure, research-question alignment, contribution mapping, terminology, claim scope, method design, evaluation evidence, related work synthesis, discussion framing, and conclusion quality.

## What It Is For

Use this skill when working on:

- CS master's thesis chapter reviews
- thesis rewrite and polishing passes
- supervisor or reviewer feedback triage
- research question and contribution audits
- evaluation design and evidence-boundary checks
- converting implementation work into academic thesis prose
- checking that claims are scoped to actual evidence

The skill is intentionally general. It does not assume a specific university, topic, supervisor, project, or thesis template.

## Repository Layout

```text
cs-thesis-reviewer/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── general-context.md
```

- `SKILL.md`: the main skill entrypoint with trigger description, workflow, output formats, and chapter-level checks.
- `references/general-context.md`: the detailed English reference for general CS master thesis writing and review rules.
- `agents/openai.yaml`: optional Codex UI metadata.

## Install for Claude Code

Claude Code can use this as a standalone skill by placing the repository under `~/.claude/skills/`.

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/1carusalwayswa/cs-thesis-reviewer.git ~/.claude/skills/cs-thesis-reviewer
```

If you already cloned the repository elsewhere, symlink it instead:

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/cs-thesis-reviewer ~/.claude/skills/cs-thesis-reviewer
```

Then restart Claude Code or reload skills if your session supports reloads.

Example prompt:

```text
Use the cs-thesis-reviewer skill to review this thesis introduction for RQ alignment, claim scope, and chapter flow.
```

## Install for Codex

Codex can use this as a skill by placing the repository under `$CODEX_HOME/skills`. If `CODEX_HOME` is not set, use `~/.codex/skills`.

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/1carusalwayswa/cs-thesis-reviewer.git "${CODEX_HOME:-$HOME/.codex}/skills/cs-thesis-reviewer"
```

Example prompt:

```text
Use $cs-thesis-reviewer to triage this supervisor feedback and turn it into a thesis revision plan.
```

## Usage Guidance

For small wording or local paragraph edits, the agent can usually follow `SKILL.md` directly.

For full chapter reviews, feedback triage, RQ planning, evaluation audits, or claim-scope checks, the agent should also read:

```text
references/general-context.md
```

Project-specific instructions always take priority over the general rules in this skill, including:

- university rules and thesis templates
- supervisor or examiner feedback
- project-specific terminology and glossary files
- real implementation status
- verified experiment or study evidence
- required writing language

## What the Skill Checks

The skill focuses on high-risk thesis problems:

- research object is unclear
- RQs do not map to contributions
- terminology is undefined or drifting
- claims exceed evidence
- Method reads like a script log
- Design reads like an implementation manual
- Evaluation lacks evidence admission or aggregation rules
- Related Work summarizes papers without synthesis
- captions replace surrounding prose
- Discussion starts with limitations instead of contribution
- Conclusion introduces new concepts or evidence

## Notes

This is a standalone skill repository. It is not a Claude Code plugin and does not require a `.claude-plugin/plugin.json` file.

The same `SKILL.md` structure is usable by both Claude Code skill loading and Codex skill loading.
