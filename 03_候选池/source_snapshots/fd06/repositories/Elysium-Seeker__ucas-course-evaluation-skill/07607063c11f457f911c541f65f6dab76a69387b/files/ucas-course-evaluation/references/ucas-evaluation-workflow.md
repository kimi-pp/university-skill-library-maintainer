# UCAS Evaluation Workflow Reference

## Page And API Shape

The UCAS evaluation front end has historically used these endpoints on `https://bkkcpj.ucas.ac.cn`:

- `GET /ea00031/findAllTerms`
- `POST /myCourse/list` with query parameters such as `title`, `pollTypeId`, `type`, and `termId`
- `GET /myPoll/getById?id=<pollId>&courseId=<courseId>`
- `POST /myPoll/submit` with the questionnaire JSON as the request body

Verify these endpoints from the current front-end bundle or network log when possible. Do not assume they are permanent.

## Common Form Types

Question `type` values observed in the Vue front end:

- `1`: single choice, answer stored in `question.answer`
- `2`: multiple choice, answers stored in `question.answers`
- `3`: text answer, stored in `question.answer`
- `4`: score/single choice, stored in `question.answer`
- `5`: matrix score, each row stored in `question.options[].answer`
- `6`: matrix single choice, each row stored in `question.options[].answer`
- `7`: matrix multiple choice, each row stored in `question.options[].answers`

Custom "other" fields may use `answer2`. Avoid selecting custom options unless the draft includes the required custom text.

## Browser Strategy

1. Try the current browser if a browser tool can reliably click and read the page.
2. If browser automation times out, use a separate Chrome profile with remote debugging.
3. Navigate through SEP's portal entry rather than going directly to `bkkcpj` if direct navigation fails.
4. Execute API reads in the page context with `fetch(..., { credentials: "include" })`.

Do not copy browser cookie databases unless absolutely necessary. If you must inspect session state, never print secret cookie values.

## Draft Validation Checklist

Before asking the user to confirm submission:

- selected term is the current evaluation term
- course count matches the page
- every required visible question has an answer
- factual questions have a known answer or an explicit assumption
- open-ended answers match the question wording
- no raw tokens or personal IDs are present in preview artifacts
- the user-facing preview explains the fill policy

## Troubleshooting

- If `/json` from the CDP port is empty, confirm Chrome was launched with `--remote-debugging-port`.
- If the app stays on SEP, click or navigate through the SEP portal link for 本科课程评价.
- If `collect` returns login HTML or redirects, the bkkcpj app is not authenticated; return to SEP and open the app from the portal.
- If submission returns HTTP 200 but a non-200 JSON `code`, stop and report the message.
- After successful submit, always run `verify` or collect the list again.
