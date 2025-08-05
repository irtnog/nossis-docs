# Contributing

This project implements
[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) using
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
The project practices [test-driven development](https://tdd.mooc.fi/)
in
[Git feature (topic) branches](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)
to maintain a [linear commit history](https://archive.is/VpWTs).
Changes must be self-contained and buildable, with updated tests and
documentation.  Please rebase changes on the latest HEAD of the main
branch before submitting them for review as a
[GitHub pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests).

A commit's scope **SHOULD** be the second-level Python module name
sans the top-level prefix or any suffixes.  For
[dunder](https://wiki.python.org/moin/DunderAlias) modules, use their
names sans underscores, e.g., `main` instead of `__main__`.
Functional test changes should use the scope of the module being
exercised, while changes to integration tests **MUST NOT** specify a
scope.


### [Refer to the developer guidance for more information.](https://irtnog.github.io/nossis-docs/en/latest/contributing.html)
