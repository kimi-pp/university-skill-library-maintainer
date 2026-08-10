---
name: ucas-course-evaluation
description: Safely assist with UCAS undergraduate course evaluations in SEP / 本科课程评价 / 期末课程评估. Use when a user asks Codex to find UCAS course evaluation forms, inspect the current semester's evaluation list, draft answers, automate filling, or submit after explicit confirmation. Includes a Chrome DevTools Protocol helper for logged-in browser sessions, draft preview generation, irreversible-submit guardrails, and post-submit verification.
---

# UCAS Course Evaluation

Use this skill to help a user complete UCAS 本科课程评价 from a logged-in SEP session while preserving a strict preview-and-confirm workflow.

## Safety Rules

- Treat final submission as irreversible. Stop before `submit` unless the user has explicitly confirmed in the current conversation.
- Do not print, save into repo files, or expose cookies, tokens, `JSESSIONID`, `Admin-Token`, or profile databases.
- Do not invent negative or personal feedback. If the user wants "quick positive" evaluation, make that assumption explicit in the preview.
- Treat factual questions separately from opinion questions. For example, "本课程是否有助教？" should be answered from user/course evidence or called out as an assumption.
- Save raw API responses and drafts only in a local `work/` folder outside the skill repo unless the user asks for a sanitized artifact.

## Recommended Workflow

1. Confirm the user is logged into SEP in Chrome or the in-app browser.
2. Open the official notice if the evaluation window or route is uncertain. Record concrete dates and the required term.
3. Reach the evaluation app through SEP, usually:
   `SEP -> 常用系统 -> 本科课程评价 -> 期末课程评估`.
4. Use Browser automation when it is reliable. If it times out, launch or attach to Chrome with remote debugging and use `scripts/ucas_eval_cdp.js`.
5. Collect course list and questionnaire JSON without submitting.
6. Generate a draft and a Markdown preview. Review:
   - course count and unfilled count
   - term name
   - factual questions
   - open-ended answers
   - required blanks
7. Ask for explicit final confirmation. Mention that submission cannot be modified afterward.
8. Submit only after confirmation.
9. Re-query the course list and report `unfilledCount` and each course's `voted` state.

## CDP Helper

The bundled helper can control a Chrome tab that was launched with remote debugging:

```powershell
chrome.exe --remote-debugging-port=9222 --user-data-dir="$PWD\work\chrome-ucas-profile" --new-window https://sep.ucas.ac.cn/appStoreStudent
```

Then run commands from a scratch workspace, not from inside the skill directory:

```powershell
node path\to\ucas-course-evaluation\scripts\ucas_eval_cdp.js status
node path\to\ucas-course-evaluation\scripts\ucas_eval_cdp.js navigate --portal-url "<SEP portal link>"
node path\to\ucas-course-evaluation\scripts\ucas_eval_cdp.js collect --out work\ucas-eval-raw.json
node path\to\ucas-course-evaluation\scripts\ucas_eval_cdp.js draft --raw work\ucas-eval-raw.json --out work\ucas-eval-draft.json --preview outputs\course_eval_preview.md --quick-positive
node path\to\ucas-course-evaluation\scripts\ucas_eval_cdp.js submit --draft work\ucas-eval-draft.json --i-understand-submit-is-final
node path\to\ucas-course-evaluation\scripts\ucas_eval_cdp.js verify
```

Prefer `--quick-positive` only when the user asked for a positive/default evaluation. Otherwise, edit or regenerate the draft from user-provided preferences.

## Filling Guidance

For common UCAS questionnaires:

- single choice and score questions: select the strongest positive option for a quick-positive draft, such as `非常符合`, `非常同意`, `非常满意`, `会`
- time-investment questions: do not blindly choose the maximum unless the user wants quick-positive assumptions; otherwise ask or leave a warning
- open-ended course feedback: include one sentence of concrete positive feedback plus one mild improvement suggestion
- lecture questions: answer the actual prompt:
  - "哪场讲座印象深刻" -> describe a field/topic the user likely attended or ask if unknown
  - "希望哪个领域" -> list fields, not an evaluation sentence
  - "哪方面需要改进" -> scheduling, reference materials, interaction time, or notice clarity

See `references/ucas-evaluation-workflow.md` for API shapes, validation notes, and troubleshooting.

## Completion Report

After submission, report concisely:

- how many forms were submitted successfully
- any API errors or courses left unfilled
- final verification result, especially `unfilledCount = 0` and `voted: true`
