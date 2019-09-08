# flake8: noqa
from pathlib import Path
from npm.bindings import npm_run
from invoke import task
from rellu import Version

assert Path.cwd() == Path(__file__).parent

VERSION_PATTERN = "__version__ = \"(.*)\""
VERSION_PATH = Path("src/SeleniumTestability/version.py")


@task
def set_version(ctx, version):
    """Set project version in ``src/SeleniumTestability/version.py`` file.
    Args:
        version: Project version to set or ``dev`` to set development version.
    """
    version = Version(version, VERSION_PATH, pattern=VERSION_PATTERN)
    version.write()
    print(version)


@task
def print_version(ctx):
    """Print the current project version."""
    print(Version(path=VERSION_PATH, pattern=VERSION_PATTERN))


@task
def webdrivers(ctx):
    """Downloads required webdrivers"""
    ctx.run("webdrivermanager firefox chrome")


@task
def generate_js(ctx):
    """Generates testability.js which is required to be done before sdist"""
    npm_run("install", "--silent")
    npm_run("run", "build", "--silent")


@task
def test(ctx):
    """Runs robot acceptance tests"""
    ctx.run("flake8")
    ctx.run("robot --outputdir output/ --loglevel TRACE:TRACE atest/")


@task
def docs(ctx):
    """Generates keyword docs"""
    ctx.run("PYTHONPATH=src python -m robot.libdoc SeleniumLibrary::plugins=SeleniumTestability docs/keywords.html")
    ctx.run("cp docs/keywords.html docs/index.html")


@task
def mypy(ctx):
    """Runs mypy against the codebase"""
    ctx.run("mypy --config mypy.ini")


@task
def black(ctx):
    """Reformat code with black"""
    ctx.run("black -l130 -tpy36 src/")


@task(pre=[generate_js, black, docs])
def build(ctx):
    """Generates dist tar ball"""
    ctx.run("python setup.py sdist")
