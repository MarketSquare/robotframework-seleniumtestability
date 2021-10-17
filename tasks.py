# flake8: noqa
from pathlib import Path
from invoke import task
from pathlib import Path
import os
import shutil


QUOTE = "\"" if os.name == "nt" else "'"

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


def patch_libdoc():
    import robot.htmldata

    old_template = Path(robot.htmldata.__file__).parent / robot.htmldata.LIBDOC
    new_template = Path(__file__).parent / "assets" / "libdoc.html"
    shutil.copy(str(new_template), str(old_template))


@task
def webdrivers(ctx, geckodriver=None, chromedriver=None):
    """Downloads required webdrivers"""
    browsers = {"firefox": "latest", "chrome": "latest"}
    if geckodriver:
        browsers["firefox"] = geckodriver
    if chromedriver:
        browsers["chrome"] = chromedriver

    ctx.run(
        f"webdrivermanager firefox:{browsers['firefox']} chrome:{browsers['chrome']} --linkpath AUTO"
    )


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
    ctx.run(f"rflint --argumentfile .rflintrc atest{os.path.sep}")


@task
def docs(ctx):
    """Generates keyword docs"""
    patch_libdoc()
    ctx.run(
        f"python -m robot.libdoc --name {QUOTE}SeleniumLibrary with SeleniumTestability Plugin{QUOTE} --pythonpath src SeleniumLibrary::plugins=SeleniumTestability docs{os.path.sep}keywords.html"
    )
    cp = "cp"
    if os.name == "nt":
        cp = "copy"
    ctx.run(f"{cp} docs{os.path.sep}keywords.html docs{os.path.sep}index.html")


@task
def mypy(ctx):
    """Runs mypy against the codebase"""
    ctx.run("mypy --config mypy.ini")


@task
def black(ctx):
    """Reformat code with black"""
    ctx.run("black -l130 -tpy37 src")


@task(pre=[generatejs])
def build(ctx):
    """Generates dist tar ball"""
    ctx.run("python setup.py sdist")


@task
def cobertura(ctx, outputfile=""):
    if len(outputfile) == 0:
        outputfile = "coverage.xml"
    ctx.run("coverage html")
    ctx.run(f"coverage xml -o {outputfile}")


@task
def test(
    ctx,
    coverage=False,
    xunit=None,
    skipci=False,
    outputdir=f"output{os.path.sep}",
    tests=None,
):
    """Runs robot acceptance tests"""
    extras = ""
    if coverage:
        ctx.run("coverage erase")
    cmd = "python"
    extra = "--non-critical skipheadless"
    if xunit:
        xunit = f"--xunit {xunit}"
    else:
        xunit = ""
    if coverage:
        cmd = "coverage run"
    if tests is None:
        tests = "atest"
    if skipci:
        extras = f"{extras} --noncritical skipci --xunitskipnoncritical --exclude skipci"

    ctx.run(
        f"{cmd} -m robot --pythonpath src --outputdir {outputdir} --loglevel TRACE:TRACE {extras} {xunit} {tests}"
    )


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


# @task
# def changelog(ctx, version=None):
#     if version is not None:
#         version = f"-c {version}"
#     else:
#         version = ""
#     ctx.run(f"gcg -x -o {CHANGELOG} -O rpm {version}")
#     filter_entries(CHANGELOG)


@task
def release(ctx, version=None):
    assert version != None
    # changelog(ctx, version)
    docs(ctx)
    ctx.run(f"git add docs{os.path.sep}* {CHANGELOG}")
    ctx.run(f"git commit -m {QUOTE}New Release {version}{QUOTE}")
    ctx.run(f"git tag {version}")
    build(ctx)
