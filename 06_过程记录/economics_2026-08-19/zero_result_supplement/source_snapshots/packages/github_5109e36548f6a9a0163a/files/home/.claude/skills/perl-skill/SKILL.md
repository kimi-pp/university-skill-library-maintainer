---
name: perl
description: Full Perl development aid. Use when the user wants to create, edit, run, debug, or test Perl scripts and modules. Scaffolds files with proper headers, follows Perl best practices, executes scripts, and assists with debugging.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [action or filename]
---

# Perl Development Skill

Assist with all aspects of Perl development including creating files, writing code, running scripts, debugging, and testing.

## Creating New Files

When creating a new Perl script (.pl) or module (.pm), always include the file header from CLAUDE.md using the Perl template. Every script must begin with:

```perl
#!/usr/bin/env perl
use strict;
use warnings;
use v5.36;
```

For modules, use the standard package structure:

```perl
package MyModule;
use strict;
use warnings;
use v5.36;

# module code here

1;
```

## Running and Testing

- Run scripts with: `perl -w <script.pl>`
- Check syntax without executing: `perl -c <script.pl>`
- Run tests with: `prove -v` or `perl -Ilib t/*.t`
- Use `perl -d <script.pl>` information to help debug issues when the user asks

## Code Quality

- Always `use strict` and `use warnings`
- Prefer modern Perl idioms (v5.36+ features like `use v5.36` which enables strict, signatures, etc.)
- Use descriptive variable names following snake_case convention
- Use Perl's built-in documentation: check `perldoc` for module usage
- Prefer core modules over external dependencies when practical
- Use three-argument `open` with lexical filehandles
- Handle errors explicitly (`open my $fh, '<', $file or die "Cannot open $file: $!"`)

## Debugging

### Built-in Perl debugging
- Add `use Data::Dumper` for inspecting complex data structures
- Use `warn` for debug output to STDERR
- Check for common issues: missing semicolons, incorrect sigils, scope problems
- Run `perl -MO=Deparse <script.pl>` to see how Perl interprets the code

### Perl debugger (perl -d)
- Launch with: `perl -d <script.pl>`
- Key commands:
  - `n` (next line), `s` (step into), `c` (continue)
  - `b <line>` (set breakpoint), `B <line>` (delete breakpoint)
  - `p <expr>` (print expression), `x <expr>` (dump structure)
  - `l` (list source), `T` (stack backtrace)
  - `w <expr>` (watch expression), `R` (restart)
  - `q` (quit)
- Use `perl -d -e 0` for an interactive Perl shell

### Perl::Critic (static analysis)
- Enforces coding standards based on Perl Best Practices
- Run with: `perlcritic <script.pl>`
- Severity levels 1 (most strict) to 5 (least strict): `perlcritic --severity 3 <script.pl>`
- Use a `.perlcriticrc` file for project-specific policies
- Disable specific policies inline: `## no critic (PolicyName)`
- Install with: `cpanm Perl::Critic`

### Perl::Tidy (code formatter)
- Reformats Perl code to a consistent style
- Run with: `perltidy <script.pl>` (creates `<script.pl>.tdy`)
- In-place formatting: `perltidy -b <script.pl>`
- Use a `.perltidyrc` file for project-specific settings
- Install with: `cpanm Perl::Tidy`

### Test::More and prove (testing framework)
- Perl's standard testing framework
- Run tests with: `prove -v` or `prove -v -r t/`
- Run a single test: `prove -v t/specific_test.t`
- Test file structure:
  ```perl
  use Test::More;

  is(my_function(1, 2), 3, 'addition works');
  ok(defined $result, 'result is defined');
  like($string, qr/pattern/, 'string matches pattern');
  is_deeply(\@got, \@expected, 'arrays match');

  done_testing();
  ```
- Additional test modules:
  - `Test::Exception` -- test that code dies/lives as expected
  - `Test::Warn` -- test warning output
  - `Test::Deep` -- flexible deep structure comparison
  - `Test::MockObject` -- mock objects for unit testing

## CPAN Modules

- Install modules with: `cpanm <Module::Name>`
- Check if a module is installed: `perl -M<Module::Name> -e1`
- Prefer well-maintained, widely-used modules

## Argument Handling

- If `$ARGUMENTS` is a filename ending in `.pl` or `.pm`, work with that file
- If `$ARGUMENTS` is "new <filename>", scaffold a new file with proper headers
- If `$ARGUMENTS` is "run <filename>", execute the script and report output
- If `$ARGUMENTS` is "test", run the project's test suite
- Otherwise, treat `$ARGUMENTS` as a general Perl development request
