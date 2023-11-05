import os

import nox

os.environ.update(PDM_IGNORE_SAVED_PYTHON="1", PDM_USE_VENV="1")

PYTHON_VERSIONS = [
    "3.7",
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "3.12",
]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    session.run("pdm", "install", "-G", "test", external=True)
    session.run("pytest", "tests/")


@nox.session
def lint(session):
    session.run("pdm", "install", "-G", "lint", external=True)
    session.run("mypy", "--install-types", "--non-interactive", "src", "tests")
    session.run("ruff", ".")
