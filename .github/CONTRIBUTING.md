# Contributing to logging-extras

Thanks for taking the time to contribute! This document describes how to get
set up and what we expect from a contribution so review stays quick and the
codebase stays consistent.

## Reporting issues

- Search [existing issues](https://github.com/zobayer1/logging-extras/issues)
  first to avoid duplicates.
- Open a new issue using one of the [issue templates](https://github.com/zobayer1/logging-extras/issues/new/choose)
  (bug, feature, improvement, or question) and fill it in completely.
- For suspected security vulnerabilities, follow the
  [security policy](SECURITY.md) instead of opening a public issue.

## Development setup

Use a virtual environment. Install the package with the development extras and
set up the pre-commit hooks:

```bash
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
pre-commit install
```

## Code style

Formatting and import order are enforced by [pre-commit](https://pre-commit.com/)
(black and isort, line length 120). Run the hooks before pushing:

```bash
pre-commit run --all-files
```

## Tests

Tests are required for every change that touches behavior — new features **and**
bug fixes (a bug fix should include a regression test that fails without the fix).

- Run the suite with coverage:

  ```bash
  pytest --cov logging_
  ```

- Run against every supported interpreter (Python 3.8–3.15) before opening a PR:

  ```bash
  tox -p auto
  ```

- Keep coverage from regressing. New code should be covered; if a line genuinely
  cannot be tested, mark it with `# pragma: no cover` and say why in the PR.

## Documentation

- Update the docstrings and the pages under `docs/` when you change public
  behavior.
- Add an entry to [`CHANGELOG.rst`](../CHANGELOG.rst) under the unreleased
  section describing your change.

## Pull requests

- Branch off `main` and keep each PR focused on a single change.
- **Link the related issue(s)** in the PR description using closing keywords so
  they close automatically on merge, e.g. `Closes #123` / `Fixes #123`.
- Fill in the [pull request template](PULL_REQUEST_TEMPLATE.md), including the
  checklist (tests, coverage, documentation).
- Make sure CI is green (tests across all supported versions and pre-commit).
- Write a clear title and description; explain the *why*, not just the *what*.

## Supported Python versions

This project supports Python 3.8 through 3.15. Please make sure changes work
across that range — `tox` covers all of them.

## Code of Conduct

By participating, you are expected to uphold our
[Code of Conduct](CODE_OF_CONDUCT.md).
