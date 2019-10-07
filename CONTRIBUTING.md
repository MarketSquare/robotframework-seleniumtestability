# Working with SeleniumTestability

## Build & Development Requirements

- nodejs and npm
   - required for downloading and bundling browser code required.
- python >= 3.6
- firefox & chrome
  - webdrivers for both browsers. Instructions to install provided.


## Workflow

First off, you you know what you are doing, go with it but here's
how the project is set up: When all dependencies are installed, all
important tasks to test, build and release can be done via pyinvoke
tool. It's like "make" but, dummer :D  When running `inv` tool to
invoke any of the thse provided tasks, the actual command will be
shown. So that if you want to do something more, you have some
reference on how to extend upon what is being laid down.

Worth to mention is that I tend to work using venv for my dev
environment needs so things might not be optimal for your needs.

Your workflow might differ but i hope you a gist ;D But here's
mine ...


### Generate and activate venv

Clone the repo and cd inside to it and execute following commands:

```bash
python3 -mvenv venv       # Generates the virtual env
source venv/bin/activate  # activates it!
```

### Install dependencies
All project dependencies are listed in root level requirements.txt
and requirements-dev.txt files. These can be used to download and
install into previously activated virtual env via:

```bash
pip install -r requirements-dev.txt
```

This will install all development time dependencies but also runtime
dependencies from requirements.txt file.

## Architecture

SeleniumTestability is build on top of new SeleniumLibrary plugin api.
Main entry point in code is plugin.py in the source folder. When this
plugin is initialized, it will tell SeleniumLibrary that it needs to 
wrap provided EventFiringWebDriver listener into it. This is listener
like api that provides before/after hooks for events that selenium 
is creating.

Thru these events, underlying system under test can be instrumented
with provided javascript code that allows the tester to avoid making 
costly sleeps or waits into test cases.

Listener code interacts with plugin via getting a reference of running
SeleniumLibrary (where our plugin lives), plugin exposes a reference of
itself and its properties via shared ctx context.

Provided javascript assets are build from assets/build.js with npm 
tooling.

There are few more "core" files in the repo. javascript.py is essentially
just a lookup table of javascript calls from within SeleniumTestability. 
logger.py for setting things up for logger and types.py to hold all custom
types.

## Building and Testing

After all development time dependencies have been installed, your
activated virtual environment shoud have a command `inv` available.
You can give `inv` commands to execute.  These commands provide
shortcuts to runn different tasks like running tests or building
javascript assets to building releases.

In order to know what tasks are currently available:

```bash
inv --list
```

and using one:

```bash
inv flake
```

Some of the tasks can accept parameters. Refer to tasks.py in the
root of the repository and pyinvoke documentation for more details.

At this point, if your shell is activated into virtual environment,
you can add/modify any project file and run existing or add new
tests.

### Build

```bash
inv generatejs
```

#### Test

First, tests are being setup in a way that they do not need to be installed
via pip. SeleniumTestability plugin is being loaded with relative paths
from the actual tests.

Before running the tests, you should have chrome & firefox and suitable
webdrivers for both the the browsers. To install webdrivers for *latest*
browser versions into previously  activated virtual enviroment:

```bash
inv webdrivers
```
If your browser versions are not the latest, you can also specify webdriver
versions for inv with `--geckodriver=version` and `--chromedriver=version`
flags.

After that, run the tests:

```bash
inv test
```

Do note that there are also typing and linting checks that should
pass:

```bash
inv flake mypy rflint
```

Configuration for these tools are in `setup.cfg`, `mypy.ini` and `.rflintrc`

### Pull Requests

Yes please! Only thing i ask is that the code follows conventions set
by the provided tooling. This means:

 * Do provide acceptance tests
 * Tests must pass.
 * Try to avoid lowering the total code coverage.
 * When submitting a PR, you can have multiple pull requests within 
   the pull request, but after the review, commits should be squashed into
   a single commit.
 * Reference the issue you are addressing in the commit message.

### Release

After verifying that that tests do pass, following comand will make all
necessary preparetions from generating changelog, build docs, change the
version number and commit everything to current branch along with required
version tag:


```bash
inv release --version=VERSION
```

Nothing get's pushed at this point so you are free to "experiment".

After the release task, use `inv build` to make the release packages and
publish to pypi with `twine`

## Coding Guideles

* mypy checks via `inv mypy` have to pass
* flake8 checks via `inv flake` have to pass
* New features require new tests.
* New tests has to pass `inv rflint`
* Format the code via  `inv black`

