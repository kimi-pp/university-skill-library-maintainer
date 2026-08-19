---
name: canvas-study-agent
description: Daily Canvas study assistant. Use when the user provides a Canvas base URL and a temporary Canvas token and asks to check Canvas courses, download new course materials, summarize lectures, classify assignments, or prepare assignment drafts. Synchronizes course data, downloads new materials, classifies assignments, and prepares minimal per-assignment workspaces. Course-level notes and end-of-session reports are opt-in, not automatic.
---

# Canvas Study Agent

## Purpose

Use this skill when the user provides a Canvas base URL and a temporary Canvas token, and asks to check Canvas courses, download new course materials, summarize course content, classify assignments, or prepare assignment drafts.

This skill turns Claude Code into a daily Canvas study assistant. The assistant should synchronize course data, download new materials, classify assignments, and prepare drafts or code solutions — but never submit work on the user's behalf.

## Security Rules

- Treat the Canvas token as temporary and sensitive.
- Never save the token to disk — not in `.env`, not in cache, not in logs, not in `user_config.json`.
- Never print the token in logs, markdown reports, code comments, or terminal output.
- Never include the token in generated files.
- Use the token only for the current session, then discard it from context.
- Never submit assignments automatically.
- Never modify Canvas data unless the user explicitly asks.
- Do not impersonate the user in quizzes, exams, or live submissions.

## Required Input

The user should provide:

- Canvas base URL, for example: `https://school.instructure.com`
- Temporary Canvas token

If either is missing, ask the user to provide it before running any script.

Pass the token to scripts via environment variables only:

```
CANVAS_BASE_URL="..." CANVAS_TOKEN="..." python <script>
```

## First-time setup is mandatory

`data/user_config.json` is the source of truth for **which courses to track** and **per-course rules**. All scripts (`sync_canvas.py`, `download_files.py`, `classify_assignment.py`, `prepare_assignment.py`, `update_course_notes.py`) refuse to run when this file is missing — they exit with a hint to run `/canvas-init`.

`/canvas-init` is interactive (driven by Claude). It (1) bootstraps a one-shot Canvas sync to populate the course list, (2) asks the user to pick courses, (3) asks per-course rules (submission medium, language, repo path, download_files preference, free-form notes), then (4) writes `data/user_config.json`. **The agent must ask every question from scratch — never pre-fill answers from memory, prior sessions, or `course_profiles.md`.** The token never lands on disk during this flow.

`sync_canvas.py --bootstrap` is the only way to run the sync without user_config; use it once during init.

## Course-specific rules — order of precedence

For any assignment work:

1. **Only** read `data/user_config.json` for `submission`, `language`, `repo_path`, `download_files`, `notes` of the course. This is the single source.
2. `course_profiles.md` holds **course-agnostic** safety / structural policies only (no per-course defaults). Apply those policies to every course.
3. If a field is missing in `user_config.courses[<id>]`, ask the user — do not infer from memory.

Hard rule across all courses: **never run git commands** on the user's behalf — they handle commits, pushes, branches themselves.

## Reading course materials and screenshots

Before drafting a solution, learn the relevant material:

1. For each PDF / PPT in the assignment's course `materials/` folder that looks relevant, run the `ocr` skill (`python .claude/skills/ocr/scripts/ocr.py <file>`). For text-based PDFs this is a fast direct extraction; for image-based PDFs it falls back to PaddleOCR.
2. The `.ocr.txt` files cache next to the original. On later runs the cache is reused unless the source changed.
3. When the user pastes a screenshot of a textbook problem (common for 微观经济学 and 计量经济学), save the image into the assignment's `attachments/` folder (creating it on demand — the prepare step does NOT create it preemptively) and run `ocr.py` on it before answering. Read both the OCR text **and** the original image, because formulas and figures often OCR badly.

## Slim Daily Workflow (`/canvas-all`)

When the user provides a Canvas token and asks to process Canvas, run these steps in order. Each step is one or more Bash commands; do not skip ahead.

1. **Pre-flight**: confirm `data/user_config.json` exists; otherwise stop and tell the user to run `/canvas-init`.

2. Sync Canvas state.
   ```
   CANVAS_BASE_URL="..." CANVAS_TOKEN="..." python .claude/skills/canvas-study-agent/scripts/sync_canvas.py
   ```
   Restricted to `selected_course_ids`.

3. Read `data/today_canvas_sync.json` and surface to the user (only for selected courses):
   - new courses (rare; if any, suggest re-running `/canvas-init`)
   - new assignments
   - changed assignments (description, due date, points, submission types)
   - changed due dates
   - new files
   - missing submissions
   - upcoming deadlines (next 7 days)

4. Download new materials, honoring per-course `download_files=false`.
   ```
   CANVAS_BASE_URL="..." CANVAS_TOKEN="..." python .claude/skills/canvas-study-agent/scripts/download_files.py
   ```

5. Classify assignments (excludes already-submitted and >24h-past-due).
   ```
   python .claude/skills/canvas-study-agent/scripts/classify_assignment.py
   ```

6. Prepare minimal per-assignment workspaces.
   ```
   python .claude/skills/canvas-study-agent/scripts/prepare_assignment.py
   ```
   See **Assignment Workspace Layout** below.

7. Read newly downloaded materials yourself (PDF, slides, code, instructions) for the assignments you'll work on. Use `ocr.py` for image-based PDFs and screenshots.

8. Process active future assignments by priority — **and apply the rule from `user_config.courses[<id>]` for each one**:
   1. due within 24 hours
   2. due within 3 days
   3. coding assignments with complete starter files
   4. assignments with newly uploaded relevant materials
   5. long writing assignments
   6. general future assignments
   7. assignments missing problem text — only remind the user, never guess

   When drafting:
   - Coding → write code into `user_config.courses[<id>].repo_path/<safe_name>/`. Do not git.
   - Theory / general → overwrite the `## 解答` section of the assignment's `solution.md` with the full step-by-step derivation. The file IS the final submission.
   - Essay → overwrite the `## 正文` section of `solution.md` with the full prose.
   - Quiz / exam → never auto-complete; offer a study plan only.

9. **No mass reports.** Do **not** auto-generate `daily_report.md`, `assignment_progress.md`, or a global `questions_for_user.md` digest. Give the user a short verbal summary in the conversation only. (`workspace/questions_for_user.md` is still appended to by the prepare step for textbook-screenshot-required items, but it is not a "report".)

Course-level notes (`cumulative_notes.md`, `course_summary.md`, `material_index.md`, `course_updates.md`) are **opt-in**: run `update_course_notes.py` (or invoke `/canvas-notes`) only when the user explicitly asks.

## Assignment Workspace Layout (minimal)

For each active future assignment of a selected course, `prepare_assignment.py` creates exactly one file per assignment, depending on classification:

| Classification | File created | Notes |
|----------------|--------------|-------|
| `coding` | `README.md` | Header pointing at `repo_path/<safe_name>/`. The actual code lives in the repo, not here. |
| `theory_problem_set` | `solution.md` | Header + Canvas description excerpt + empty `## 解答` block. The user submits this file (or hand-copies it). |
| `essay_report` | `solution.md` | Header + Canvas description excerpt + empty `## 正文` block. |
| `general` | `solution.md` | Same shape, generic prompt. |
| `textbook_screenshot_required` | (none) | Adds one line to `workspace/questions_for_user.md`. The folder is created later, only after the user uploads the screenshot. |
| `quiz_exam` | (none) | Skipped. |

The prepare step **does not** create:

- `assignment_summary.md`
- `submission_checklist.md`
- `relevant_course_materials.md`
- per-assignment `questions_for_user.md`
- empty `attachments/` directory
- `assignment_raw.json` (the same data is in `data/assignment_index.full.json`)

When Claude needs to OCR a screenshot belonging to a specific assignment, it creates `attachments/` on demand at that moment.

Existing assignment folders (those already filled in before this slim refactor) are left untouched. New rules apply only to new assignments.

## Classification types

`data/classification_index.json` labels each eligible assignment with one of:

- `coding`
- `theory_problem_set`
- `essay_report`
- `textbook_screenshot_required`
- `quiz_exam`
- `general`

Classification skips already-submitted and >24h-past-due assignments.

### Coding Assignment

Trigger: programming keywords, starter code, GitHub links, attachments like `.py`, `.ipynb`, `.java`, `.cpp`, `.R`, `.zip`, or test files.

1. Read assignment `README.md` and the Canvas description.
2. Implement code at `user_config.courses[<id>].repo_path/<safe_name>/` — not in the canvas workspace.
3. Run tests if available. If tests fail, debug and retry.
4. **Do not** create `run_instructions.md`, `test_report.md`, `submission_checklist.md` etc. Keep notes inline in code comments or a short README *in the repo* if needed.
5. Do not submit automatically. Do not git.

### Theory / Problem Set Assignment

Trigger: math, statistics, finance, econometrics, ML theory, derivations, problem sets.

1. Identify and read relevant course materials (slides, lecture notes, PDFs).
2. Overwrite the `## 解答` section of `solution.md` with a complete, step-by-step derivation. Final answer should be clearly highlighted.
3. Mark uncertain steps with `> Uncertain:` blockquotes.
4. If the problem statement is incomplete, append to `workspace/questions_for_user.md` and stop.

### Essay / Report Assignment

Trigger: essay, report, reflection, discussion post, literature review, written response.

1. Read relevant course materials.
2. Overwrite the `## 正文` section of `solution.md` with the finished essay.
3. Mark places where the user must add personal views or class-specific details with `> TODO:` blockquotes.

### Textbook Screenshot Required

Trigger: assignment references textbook chapters, pages, or problem numbers but Canvas does not include the full problem text.

1. Do not guess the question.
2. Do not fabricate the problem statement.
3. The prepare script has already added a line to `workspace/questions_for_user.md`.
4. Stop processing this assignment until the user uploads the screenshots. When they do, save them under `workspace/courses/<course>/assignments/<assignment>/attachments/` (creating `attachments/` then), OCR them, and proceed as a `theory_problem_set`.

### Quiz / Exam

1. Do not attempt to complete them automatically.
2. Summarize schedule, scope, due date, and review materials.
3. Generate a study plan if the user asks.

## Output Rules

- The default Canvas pipeline writes the following data files: `data/today_canvas_sync.json`, `data/course_index.json`, `data/assignment_index.json`, `data/classification_index.json`, `data/cache.json`, `data/download_report.json`, `data/user_config.json`.
- Inside the workspace, only assignment-level files (`README.md` or `solution.md`) and a global `workspace/questions_for_user.md` are auto-maintained.
- Course-level files (`cumulative_notes.md`, `course_summary.md`, `material_index.md`, `course_updates.md`) appear only after `/canvas-notes` is invoked.
- `daily_report.md` and `assignment_progress.md` are **not** generated automatically. If the user wants them, generate them on request.

## Academic Integrity Rule

The assistant helps the user understand, organize, draft, test, and review work. It must not:

- automatically submit final answers,
- complete live quizzes/exams,
- impersonate the user in Canvas,
- run git commands on the user's behalf (commits, pushes, etc.).

`solution.md` is the **draft you would actually submit** — the user is expected to review it, add personal voice where the agent inserted `> TODO:` markers, then submit / hand-copy / push themselves.
