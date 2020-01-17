# flake8: noqa
from pathlib import Path
from invoke import task
import os
from pathlib import Path
import shutil

CHANGELOG = "CHANGELOG"
filters = ["poc", "new release", "wip", "cleanup", "!nocl"]


def filter_entries(filename):
    buffer = []
    with open(filename) as old_file:
        buffer = old_file.read().split("\n")

    with open(filename, "w") as new_file:
        for line in buffer:
            if not any(bad_word in line.lower() for bad_word in filters):
                new_file.write(line + "\n")


assert Path.cwd() == Path(__file__).parent


@task
def webdrivers(ctx, geckodriver=None, chromedriver=None):
    """Downloads required webdrivers"""
    browsers = {"firefox": "latest", "chrome": "latest"}
    if geckodriver:
        browsers["firefox"] = geckodriver
    if chromedriver:
        browsers["chrome"] = chromedriver

    ctx.run("webdrivermanager firefox:{} chrome:{} --linkpath AUTO".format(browsers["firefox"], browsers["chrome"]))


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


@task(pre=[generatejs])
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
def test(ctx, coverage=False, xunit=None, skipci=False, outputdir="output/", tests=None):
    """Runs robot acceptance tests"""
    extras = ""
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
    if skipci:
        extras=f"{extras} --noncritical skipci --xunitskipnoncritical"

    ctx.run("{} -m robot --pythonpath src --outputdir {} --loglevel TRACE:TRACE {} {} {}".format(cmd, outputdir, extras, xunit, tests))


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
        fs_entry = Path(item)
        if fs_entry.is_dir():
            shutil.rmtree(item)
        elif fs_entry.is_file():
            fs_entry.unlink()
        else:
            for fs_entry in Path().glob(item):
                fs_entry.unlink()


@task
def changelog(ctx, version=None):
    if version is not None:
        version = "-c {}".format(version)
    else:
        version = ""
    ctx.run("gcg  -x -o {} -O rpm  {}".format(CHANGELOG, version))
    filter_entries(CHANGELOG)


@task
def release(ctx, version=None):
    assert version != None
    changelog(ctx, version)
    docs(ctx)
    ctx.run("git add docs/* {}".format(CHANGELOG))
    ctx.run("git commit -m 'New Release {}'".format(version))
    ctx.run("git tag {}".format(version))
    build(ctx)
