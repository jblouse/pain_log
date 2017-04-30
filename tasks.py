"""Build automation driver using invoke"""
# -*- coding: utf-8 -*-
from invoke import task


SETUP_COMMAND = 'rm -rf venv && virtualenv venv && source venv/bin/activate'
PIP_COMMAND = 'venv/bin/pip install -r requirements.pip'
LINT_COMMAND = 'venv/bin/flake8 *.py && venv/bin/pep8 *.py ' \
               '&& venv/bin/pylint *.py'
TEST_COMMAND = 'venv/bin/nosetests --with-coverage --cover-erase ' \
               '--cover-package=weather_api ' \
               '--cover-package=weather_retriever ' \
               '--cover-package=settings' \
               ' && rm -rf .coverage *.log && find . -name "*.pyc" -delete'


@task
def pip(ctx):
    """Install pip requirements"""
    ctx.run(PIP_COMMAND, hide=True)


@task
def setup(ctx):
    """Perform setup tasks"""
    ctx.run(SETUP_COMMAND, hide=True)
    pip(ctx)


@task
def lint(ctx):
    """Run lint check"""
    ctx.run(LINT_COMMAND)


@task
def test(ctx):
    """Run tests with coverage"""
    ctx.run(TEST_COMMAND)


@task(default=True)
def build(ctx):
    """Perform build"""
    lint(ctx)
    test(ctx)
