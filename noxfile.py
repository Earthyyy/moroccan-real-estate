import shutil
import nox

# Default sessions to run if no specific sessions are provided
nox.options.sessions = ["lint", "formatting", "typing", "test"]

# Centralized Python version for all sessions
PYTHON_VERSION = "3.11"

# Helper function to install Poetry dependencies
def install_poetry_dependencies(session, group=None):
    # First, check if the lock file is in sync with pyproject.toml
    session.run("poetry", "check", "--lock", external=True)

    # If it's in sync, proceed to install dependencies
    if group:
        session.run("poetry", "install", f"--only={group}", external=True)
    else:
        session.run("poetry", "install", external=True)

# Linting session using Ruff for static analysis
@nox.session(python=PYTHON_VERSION)
def lint(session):
    # Install only the lint dependencies group
    install_poetry_dependencies(session, "lint")

    # Run Ruff on both the source and test directories
    for directory in ["./src", "./tests"]:
        session.run("ruff", "check", directory)

# Formatting session using Black and Isort to check code style
@nox.session(python=PYTHON_VERSION)
def formatting(session):
    # Install only the formatting dependencies group
    install_poetry_dependencies(session, "format")

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
    # Install only the typing dependencies group
    install_poetry_dependencies(session, "typing")

    session.run("mypy", "src")

# Dev environment setup to install all dependencies for development
@nox.session(python=PYTHON_VERSION)
def dev(session):
    # Install all project dependencies
    install_poetry_dependencies(session)

    session.log("Virtual environment created and all dependencies installed.")

    # Provide activation command for different platforms
    if session.posargs and session.posargs[0] == "windows":
        session.log(r"  .\.nox\dev\Scripts\activate")
    else:
        session.log("  source .nox/dev/bin/activate")

# Documentation build session using Sphinx
@nox.session(python=PYTHON_VERSION)
def doc(session):
    # Install only the documentation dependencies group
    install_poetry_dependencies(session, "doc")

    shutil.rmtree("docs/_build", ignore_errors=True)

    if session.posargs and session.posargs[0] == "i":
        session.run("sphinx-autobuild", "docs", "docs/_build/html", "--open-browser")
    else:
        session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")

# Testing session using Pytest and Coverage
@nox.session(python=PYTHON_VERSION)
def test(session):
    install_poetry_dependencies(session)

    # Install only the testing dependencies group
    install_poetry_dependencies(session, "test")

    # Run tests and measure coverage
    session.run("pytest", "./tests")
    session.run("coverage", "run", "--source=src", "-m", "pytest", "./tests")
    session.run("coverage", "report")

    # Clean up coverage files
    shutil.rmtree(".coverage", ignore_errors=True)
