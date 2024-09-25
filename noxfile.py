"""
Noxfile for automating various development tasks such as linting, formatting,
type checking, testing, and documentation building.

How to Run Nox Sessions:
------------------------
1. To run all predefined sessions (lint, formatting, typing, test):
   $ nox

2. To run a specific session:
   $ nox -s <session_name>

   Example: To run only the linting session:
   $ nox -s lint

   Available sessions:
   - lint: Runs Ruff to check for linting issues.
   - formatting: Runs Black and Isort to check code formatting.
   - typing: Runs MyPy for static type checking.
   - dev: Sets up a development environment.
        - windows: Use when working on Windows.
   - doc: Builds documentation using Sphinx.
        - i: Use to build interactive documentation
   - test: Runs the test suite with pytest and coverage.

3. To run sessions with additional arguments (e.g., specifying platform for dev session):
   $ nox -s dev -- windows  # Example for running dev on Windows
"""

import shutil

import nox

# Default sessions to run if no specific sessions are provided
nox.options.sessions = ["lint", "formatting", "typing", "test"]

# Centralized Python version for all sessions
PYTHON_VERSION = "3.11"


# Helper function to install requirements from a file
def install_requirements(session, requirements_file):
    session.install("-r", requirements_file)


# Linting session using Ruff for static analysis
@nox.session(python=PYTHON_VERSION)
def lint(session):
    install_requirements(session, "requirements/lint-requirements.txt")

    # Run Ruff on both the source and test directories
    for directory in ["./src", "./tests"]:
        session.run("ruff", "check", directory)


# Formatting session using Black and Isort to check code style
@nox.session(python=PYTHON_VERSION)
def formatting(session):
    install_requirements(session, "requirements/format-requirements.txt")

    # Run Black and Isort on both source and test directories
    for directory in ["./src", "./tests"]:
        session.run("black", "--check", directory)
        session.run("isort", "--check", directory)


# Typing session using MyPy for static type checking
@nox.session(python=PYTHON_VERSION)
def typing(session):
    install_requirements(session, "requirements/typing-requirements.txt")
    session.run("mypy", "src")


# Dev environment setup to install dependencies for development
@nox.session(python=PYTHON_VERSION)
def dev(session):
    # Install project dependencies
    session.run("python", "-m", "pip", "install", ".[dependencies]", external=True)
    session.log("Virtual environment created and dependencies installed.")

    # Provide activation command for different platforms
    if session.posargs and session.posargs[0] == "windows":
        session.log(r"  .\.nox\dev\Scripts\activate")
    else:
        session.log("  source .nox/dev/bin/activate")


# Documentation build session using Sphinx
@nox.session(python=PYTHON_VERSION)
def doc(session):
    install_requirements(session, "requirements/doc-requirements.txt")
    shutil.rmtree("docs/_build", ignore_errors=True)

    if session.posargs and session.posargs[0] == "i":
        session.run("sphinx-autobuild", "docs", "docs/_build/html", "--open-browser")
    else:
        session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")


# Testing session using Pytest and Coverage
@nox.session(python=PYTHON_VERSION)
def test(session):
    # Install project dependencies and testing requirements
    session.run("python", "-m", "pip", "install", ".[dependencies]", external=True)
    install_requirements(session, "requirements/test-requirements.txt")

    # Run tests and measure coverage
    session.run("pytest", "./tests")
    session.run("coverage", "run", "--source=src", "-m", "pytest", "./tests")
    session.run("coverage", "report")

    # Clean up coverage files
    shutil.rmtree(".coverage", ignore_errors=True)
