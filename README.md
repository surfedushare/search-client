# Search Client

A Python wrapper around Open Search to make searching easier

## Prerequisites

This project uses `Python 3.10` and`docker-compose`.
Make sure they are installed on your system before installing the project.

#### Mac OS setup

We recommend installing Python through pyenv:

```
brew update && brew upgrade pyenv
pyenv install 3.10.4
```

#### General setup

To install the basic environment and tooling you'll need to first setup a local environment on a host machine with:

```bash
python3 -m venv venv --copies --upgrade-deps
source venv/bin/activate
pip install -r requirements.txt
```

To finish the general setup you can run this command to build Open Search:

```bash
docker-compose up --build
```

## Getting started

First you need to activate the venv:

```bash
source venv/bin/activate
```

Then you can start the Open Search service through Docker:

```bash
docker-compose up
docker-compose down
```

## Tests

You can run all tests for the entire repo by running:

```bash
invoke test.run
```

It's also possible to run specific test cases or tests by specifying them through the ``-t`` flag.

## Release and install

You can create a Github release on the Github website.
Make sure that the release tag matches the version number in ``search_client/version.py``.
It's also possible to create a tag with git directly and push that to the remote.

Once a release has been made you can specify the following in any requirements.txt to use that specific version:

```
git+https://github.com/surfedushare/search-client.git@v0.0.1
```

## Linting

The python code uses flake8 as a linter. You can run it with the following command:

```bash
flake8 .
```
