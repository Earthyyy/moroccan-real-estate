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
    if session.posargs and session.posargs[0] == "run":
        for directory in ["./src", "./tests"]:
            session.run("black", directory)
            session.run("isort", directory)
    else:
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
