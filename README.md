# Moroccan Real Estate

## Dependency management

This project uses [Poetry](https://python-poetry.org/) for dependency management. Dependencies and their versions are managed in the `pyproject.toml` file. First, you will need to install Poetry, as mentioned in the Poetry documentation. **Poetry should always be installed in a dedicated virtual environment to isolate it from the rest of your system.** The best practice is to use `pipx` to install Poetry globally while keeping it isolated in a virtual environment. Run the following command:

```bash
pipx install poetry==1.8.4
```

- To add new dependecies to the project, use: 

```bash
poetry add <package-name>
```
- To add new dependencies to a certain group (for example lint group), run:


```bash
poetry add --lint <package-name>
```

- To update the project dependencies to their latest allowed versions:
```bash
poetry update
```
---
> **_NOTE:_** This will update the dependencies based on the version constraints in `pyproject.toml` and lock the updated versions in the `poetry.lock` file.
---


## Automated CI and doc building

We use [nox](https://nox.thea.codes/en/stable/) for automating various development tasks such as linting, formatting,
type checking, testing, and documentation building.

### How to Run Nox Sessions

1. To run all predefined sessions (lint, formatting, typing, test):
   `nox`

2. To run a specific session:
   `nox -s <session_name>`

   Example: To run only the linting session:
   `nox -s lint`

   Available sessions:
   - lint: Runs Ruff to check for linting issues.
   - formatting: Runs Black and Isort to check code formatting.
        - run: Use to apply changes.
   - typing: Runs MyPy for static type checking.
   - dev: Sets up a development environment.
        - windows: Use when working on Windows.
   - doc: Builds documentation using Sphinx.
        - i: Use to build interactive documentation
   - test: Runs the test suite with pytest and coverage.

3. To run sessions with additional arguments (e.g., specifying os for dev session):

`nox -s dev -- windows` (Example for running dev on Windows)

