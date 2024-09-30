# Moroccan Real Estate

## Automated CI and doc building

Noxfile for automating various development tasks such as linting, formatting,
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
