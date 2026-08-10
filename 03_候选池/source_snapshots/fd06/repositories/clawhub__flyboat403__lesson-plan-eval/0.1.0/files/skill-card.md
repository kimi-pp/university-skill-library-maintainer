## Description: <br>
Audits Chinese vocational education lesson plans against Bloom, Gagne, Marzano, 5E, and vocational teaching standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyboat403](https://clawhub.ai/user/flyboat403) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, curriculum reviewers, and teaching researchers use this skill to audit vocational lesson plans, identify weak objectives, activities, questions, assessment alignment, and produce improvement reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional .docx export uses a Pandoc shell command that may handle user-provided filenames or documents. <br>
Mitigation: Review and quote filenames before running the command, and avoid converting untrusted paths without checking them first. <br>
Risk: The skill may activate broadly for lesson-plan quality discussions. <br>
Mitigation: Confirm the user wants a formal lesson-plan audit when the conversation only mentions general teaching quality. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyboat403/skills/lesson-plan-eval) <br>
- [Server-resolved GitHub source](https://github.com/flyboat403/lesson-plan-eval) <br>
- [Output template](references/output-template.md) <br>
- [Scoring standard](references/scoring-standard.md) <br>
- [Pandoc guide](references/pandoc-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown lesson-plan audit report with structured tables and an optional Pandoc command for .docx export.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for clarification when input contains multiple lesson plans or lacks core lesson-plan elements.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
