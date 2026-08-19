---
name: applescript
description: Full AppleScript development aid. Use when the user wants to create, edit, run, debug, compile, or test AppleScript scripts, including GUI automation via System Events. Scaffolds files with proper headers, follows AppleScript best practices, compiles and runs scripts, and assists with debugging.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [action or filename]
---

# AppleScript Development Skill

Assist with all aspects of AppleScript development including creating files, writing code, compiling, running, debugging, and testing — both application scripting (via scripting dictionaries) and GUI automation (via System Events).

## Creating New Files

When creating a new AppleScript file, always include the file header from CLAUDE.md using the **AppleScript block comment style** (`(* *)`), not `/* */`. AppleScript has no C-style comments.

- Block comments: `(* ... *)`
- Single-line comments: `--` or `#`

Use the `.applescript` extension for source and `.scpt` for compiled output.

## Compiling and Running

- Compile (syntax check, no execution): `osacompile -o /tmp/out.scpt <script.applescript>`
- Run: `osascript <script.applescript>`
- Compile to a runnable .app: `osacompile -o <name>.app <script.applescript>`

**`osacompile` catches syntax errors but NOT runtime errors.** Compiling clean does not mean the script runs — handler dispatch, missing UI elements, and permissions only surface at run time.

## Code Quality

- Use `tell ... end tell` blocks scoped as tightly as possible; do not nest unrelated work inside an application's `tell`.
- Prefer explicit element paths over `whose` filters in hot loops, but use `whose` clauses for resilience when element indices shift.
- Wrap fragile UI lookups in `try ... end try` so one missing element does not abort the whole script.
- Use `delay` after UI actions that trigger animations or sheets; GUI automation races the UI otherwise.
- Name variables descriptively; avoid one- or two-letter names — some short tokens collide with reserved words and fail to parse (e.g. a bare `rd` was rejected).

## Calling Your Own Handlers Inside a `tell` Block

**Critical, compiler-invisible bug:** inside a `tell application` / `tell process` block, an unqualified handler call like `myHandler()` is dispatched to the *target application*, not to your script. The target has no such handler, so it fails at run time even though it compiles clean.

Prefix calls to your own handlers with `my` (or `of me`):

```applescript
tell application "System Events"
    tell process "Messages"
        my deleteAllConversations()      -- dispatched to the script
        if my clickAffirmative(window 1) then return
    end tell
end tell
```

Without `my`, AppleScript tries to send `deleteAllConversations` to the Messages process and errors.

## GUI Automation (System Events)

- Requires Accessibility permission: System Settings > Privacy & Security > Accessibility, granted to the app that runs the script (Script Editor, Terminal, osascript, etc.). Every `System Events` call fails silently or errors without it.
- UI-element hierarchies (`splitter group`, `scroll area`, `table`, toolbar buttons) and menu/button titles shift between macOS releases. Treat any hardcoded path as version-specific.
- Use **Accessibility Inspector** (Xcode > Open Developer Tool > Accessibility Inspector) to confirm the live element tree and exact titles before relying on them.
- Key codes for keystrokes: `key code 51` = Delete, `key code 53` = Escape, `key code 36` = Return, `key code 0 using {command down}` = Cmd+A.

## Debugging

- Use `log "message"` statements; output appears in Script Editor's log pane or on stderr under `osascript`.
- Use `display dialog (someVariable as text)` for quick inspection of values mid-run.
- Errors report a line number and a `(-NNNN)` OSA error code — `-2741` is a parser error, `-2740` a syntax-position error, `-1728` "can't get <element>" (missing UI element), `-25211` accessibility not authorized.
- For GUI automation, isolate the failing `tell` block and run it alone to confirm the element path.

## Argument Handling

- If `$ARGUMENTS` is a filename ending in `.applescript` or `.scpt`, work with that file
- If `$ARGUMENTS` is "new <filename>", scaffold a new file with the `(* *)` header
- If `$ARGUMENTS` is "run <filename>", execute with `osascript` and report output
- If `$ARGUMENTS` is "check <filename>", compile with `osacompile` to validate syntax
- Otherwise, treat `$ARGUMENTS` as a general AppleScript development request
