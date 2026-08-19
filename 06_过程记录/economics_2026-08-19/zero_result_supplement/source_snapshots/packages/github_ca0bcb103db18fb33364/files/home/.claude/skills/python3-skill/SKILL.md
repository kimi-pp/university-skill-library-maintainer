---
name: python3
description: Full Python 3 development aid. Use when the user wants to create, edit, run, debug, or test Python scripts and packages. Scaffolds files with proper headers, follows Python best practices, executes scripts, and assists with debugging.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [action or filename]
---

# Python 3 Development Skill

Assist with all aspects of Python 3 development including creating files, writing code, running scripts, debugging, and testing.

## Creating New Files

When creating a new Python file, always include the file header from CLAUDE.md using the Python template. The shebang and encoding lines are part of the template:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

## Running and Testing

- Run scripts with: `python3 <script.py>`
- Run module: `python3 -m <module_name>`
- Check syntax: `python3 -m py_compile <script.py>`
- Run tests with: `python3 -m pytest -v` or `python3 -m unittest discover`
- Type checking: `mypy <script.py>` (if available)
- Linting: `ruff check <script.py>` or `flake8 <script.py>` (if available)

## Code Quality

- Target Python 3.10+ unless the project specifies otherwise
- Use type hints for function signatures
- Follow PEP 8 naming conventions:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_SNAKE_CASE` for constants
- Use f-strings for string formatting
- Use `pathlib.Path` over `os.path` for file operations
- Use context managers (`with` statements) for resource management
- Prefer list/dict/set comprehensions where they improve readability
- Use `dataclasses` or `NamedTuple` for data containers

## Project Structure

- For packages, ensure `__init__.py` exists
- Use `pyproject.toml` for project configuration when applicable
- Virtual environments: `python3 -m venv .venv`
- Install dependencies: `pip install -r requirements.txt`

## Debugging

### Built-in Python debugging
- Use `pprint` for readable data structure output
- Use `traceback` module for detailed exception information
- Check for common issues: indentation errors, mutable default arguments, variable scope

### pdb / breakpoint() (Python debugger)
- Insert `breakpoint()` (Python 3.7+) to drop into the debugger at that line
- Launch from command line: `python3 -m pdb <script.py>`
- Key commands:
  - `n` (next line), `s` (step into), `c` (continue), `r` (return from function)
  - `b <line>` (set breakpoint), `cl <line>` (clear breakpoint)
  - `p <expr>` (print expression), `pp <expr>` (pretty-print)
  - `l` (list source), `w` (where/backtrace), `u`/`d` (up/down frame)
  - `q` (quit)
- Use `PYTHONBREAKPOINT=0` to disable all breakpoints without removing them

### Ruff (linter and formatter)
- Fast Python linter and formatter written in Rust
- Lint: `ruff check <script.py>` or `ruff check .`
- Auto-fix: `ruff check --fix <script.py>`
- Format: `ruff format <script.py>`
- Configure in `pyproject.toml` under `[tool.ruff]`
- Install with: `pip install ruff`

### mypy (static type checker)
- Checks type annotations for correctness
- Run with: `mypy <script.py>` or `mypy .`
- Strict mode: `mypy --strict <script.py>`
- Ignore specific lines: `# type: ignore[error-code]`
- Configure in `pyproject.toml` under `[tool.mypy]`
- Install with: `pip install mypy`

### pytest (testing framework)
- Python's most widely used test framework
- Run tests with: `python3 -m pytest -v`
- Run a single file: `python3 -m pytest -v test_specific.py`
- Run a single test: `python3 -m pytest -v test_file.py::test_name`
- Test file structure:
  ```python
  import pytest

  def test_addition():
      assert my_function(1, 2) == 3

  def test_raises():
      with pytest.raises(ValueError):
          my_function(-1)

  @pytest.fixture
  def sample_data():
      return {"key": "value"}

  def test_with_fixture(sample_data):
      assert sample_data["key"] == "value"
  ```
- Key plugins:
  - `pytest-cov` -- code coverage reporting (`--cov=src`)
  - `pytest-mock` -- mock objects via `mocker` fixture
  - `pytest-xdist` -- parallel test execution (`-n auto`)

## Argument Handling

- If `$ARGUMENTS` is a filename ending in `.py`, work with that file
- If `$ARGUMENTS` is "new <filename>", scaffold a new file with proper headers
- If `$ARGUMENTS` is "run <filename>", execute the script and report output
- If `$ARGUMENTS` is "test", run the project's test suite
- Otherwise, treat `$ARGUMENTS` as a general Python development request
