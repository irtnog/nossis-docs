% nossis-docs, serverless hosting for static, private web sites that
% works like GitHub Pages
%
% Copyright (C) 2024  Matthew X. Economou
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU Affero General Public License as
% published by the Free Software Foundation, either version 3 of the
% License, or (at your option) any later version.
%
% This program is distributed in the hope that it will be useful, but
% WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
% Affero General Public License for more details.
%
% You should have received a copy of the GNU Affero General Public
% License along with this program.  If not, see
% <https://www.gnu.org/licenses/>.

# Contributing

This project combines [test-driven development](https://tdd.mooc.fi/),
[atomic commits](https://www.aleksandrhovhannisyan.com/blog/atomic-git-commits/),
a [linear commit history](https://archive.is/VpWTs), and the
[Git feature branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).
Please rebase your changes on the latest HEAD of the main branch
before submitting them for review as a
[GitHub pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests).
Changes must include updated functional and integration tests.


## Development Environment

This project requires Python 3.11 and OpenTofu 1.8 (or newer).  To set
up your development environment on Linux or macOS, run these
[GNU Make](https://www.gnu.org/software/make/) commands from the
project root directory.

{.glossary}
`make setup`
: Create (or update) a
  [Python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments)
  named `.venv` in the project root directory, and perform an editable
  installation of this project that includes development and testing
  tools.

{.glossary}
`make pre-commit`
: Configure optional pre-commit hooks, which require the virtual
  environment to be active in your code editor or
  [Git porcelain](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain).

{.glossary}
`make clean`
: Reset the development environment, which includes removing the
  pre-commit hooks.

Additional targets are available, several of which are listed below.
Review the makefile for details.

{.glossary}
`make lint`
: Check code syntax and style.

{.glossary}
`make test`
: Perform comprehensive functional and integration testing.

{.glossary}
`make smoke`
: Run a shorter, faster subset of the test suite.


## Code Style

This project follows these code styles:

- [OpenTofu style conventions](https://opentofu.org/docs/language/syntax/style/)

- [Python Black](https://black.readthedocs.io/)
  and [isort](https://pycqa.github.io/isort/)

- [the Google Markdown style guide](https://google.github.io/styleguide/docguide/style.html),
  but with a more traditional 70-character line limit

- [the Home Assistant YAML style guide](https://developers.home-assistant.io/docs/documenting/yaml-style-guide/)


## Commit Messages

This project implements
[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) using
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
Please use English in commit messages.  The first line of the commit
message should be at most 100 characters, while the rest of the commit
message should be wrapped at column 70.  A commit's description should
be a verb phrase in the imperative present tense, with the starting
verb in lower case and no ending punctuation.

Valid commit types are:

{.glossary}
`build`
: changes to the build system or external dependencies

{.glossary}
`chore`
: miscellaneous changes not covered by the other commit types

{.glossary}
`ci`
: changes to the continuous integration/continuous delivery process,
  e.g., GitHub Actions

{.glossary}
`docs`
: documentation-only changes

{.glossary}
`feat`
: a new feature

{.glossary}
`fix`
: a bug fix

{.glossary}
`perf`
: a code change that improves performance

{.glossary}
`refactor`
: a code change that neither fixes a bug nor adds a feature

{.glossary}
`style`
: a code change that only affects formatting

{.glossary}
`test`
: new tests or corrections to existing tests

Do not specify a scope for changes covering multiple scopes or for
changes not specific to one scope.  Otherwise, a commit's scope should
be the second-level OpenTofu or Python module name sans the top-level
prefix or any suffixes.  For top-level
[dunder](https://wiki.python.org/moin/DunderAlias) modules, use their
names sans the double underscores as the scope, e.g., `init` for
`__init__.py`.
