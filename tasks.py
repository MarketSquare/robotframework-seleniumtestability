# flake8: noqa
from pathlib import Path
from invoke import task
from rellu import Version
import os
import os.path
import shutil
import glob

assert Path.cwd() == Path(__file__).parent

VERSION_PATTERN = '__version__ = "(.*)"'
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
def webdrivers(ctx, geckodriver=None, chromedriver=None):
    """Downloads required webdrivers"""
    browsers = {'firefox': 'latest', 'chrome': 'latest'}
    if geckodriver:
        browsers['firefox'] = geckodriver
    if chromedriver:
        browsers['chrome'] = chromedriver

    ctx.run("webdrivermanager firefox:{} chrome:{} --linkpath AUTO".format(browsers['firefox'], browsers['chrome']))


@task
def generatejs(ctx):
    """Generates testability.js which is required to be done before sdist"""
    ctx.run("npm install")
    ctx.run("npm run build")


@task
def flake(ctx):
    """Runs flake8 against whole project"""
    ctx.run("flake8")


@task
def rflint(ctx):
    """Runs rflint agains atests"""
    ctx.run("rflint --argumentfile .rflintrc atest/")


@task
def docs(ctx):
    """Generates keyword docs"""
    ctx.run("python -m robot.libdoc --pythonpath src SeleniumLibrary::plugins=SeleniumTestability docs/keywords.html")
    ctx.run("cp docs/keywords.html docs/index.html")


@task
def mypy(ctx):
    """Runs mypy against the codebase"""
    ctx.run("mypy --config mypy.ini")


@task
def black(ctx):
    """Reformat code with black"""
    ctx.run("black -l130 -tpy36 src/")


@task(pre=[generatejs, black, docs])
def build(ctx):
    """Generates dist tar ball"""
    ctx.run("python setup.py sdist")


@task
def cobertura(ctx, outputfile=""):
    if len(outputfile) == 0:
        outputfile = "coverage.xml"
    ctx.run("coverage html")
    ctx.run("coverage xml -o {}".format(outputfile))


@task
def test(ctx, coverage=False, xunit=None, outputdir="output/", tests=None):
    """Runs robot acceptance tests"""
    if coverage:
        ctx.run("coverage erase")
    cmd = "python"
    extra = ""
    if xunit:
        xunit = "--xunit {}".format(xunit)
    else:
        xunit = ""
    if coverage:
        cmd = "coverage run"
    if tests is None:
        tests = "atest/"
    ctx.run("{} -m robot --pythonpath src --outputdir {} --loglevel TRACE:TRACE {} {}".format(cmd, outputdir, xunit, tests))


@task
def clean(ctx):
    to_be_removed = [
        ".mypy_cache/",
        "coverage_report/",
        "dist/",
        "monkeytype.sqlite3",
        "node_modules/",
        "output/",
        "src/robotframework_seleniumtestability.egg-info/",
        "output.xml",
        ".coveragedb",
        "*.html",
        "selenium-screenshot-*.png",
        "geckodriver-*.log",
        "assets/std*.txt",
    ]

    for item in to_be_removed:
        if os.path.isdir(item):
            shutil.rmtree(item)
        elif os.path.isfile(item):
            os.remove(item)
        else:
            for filename in glob.glob(item):
                os.remove(filename)
