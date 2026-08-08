## Description: <br>
Review academic degree theses with a structured evaluation framework supporting bachelor, master, and PhD theses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Academic reviewers, supervisors, and thesis committees use this skill to extract thesis details, assess innovation, methodology, experiments, writing quality, and produce structured review feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes thesis documents that may contain unpublished research or personal information. <br>
Mitigation: Confirm the thesis input is appropriate to share with the active agent and avoid including unnecessary sensitive material. <br>
Risk: The skill creates a Word review file locally and repeated reviews can overwrite or confuse similarly named files. <br>
Mitigation: Confirm the requested output path and filename before creating the document, especially for repeated reviews of the same author on the same date. <br>
Risk: Literature comparisons based on web search can miss relevant work or overstate novelty. <br>
Mitigation: Verify important external claims and citations before relying on the final review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/thesis-review) <br>
- [Review patterns](artifact/references/review-patterns.md) <br>
- [Review templates](artifact/references/review-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance, files] <br>
**Output Format:** [Structured Markdown review feedback plus a local .docx review file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use web search for literature comparison and creates a Word document using a reviewer-confirmed output path and filename.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
