# dummy-excel-generator

## Description

This is a POC for generating dummy Excel files with fake data.

The generated Excel files can be used to test the condition when row count exceed the limit of 1048576, so it won't be able to open.

In our case, we were testing against **OPSWAT**'s CDR (Content Disarm and Reconstruction) technology, which can detect and reconstruct malicious Excel files.

## How it works

1. Generate a list of fake data(`dictionary`) with [Faker](https://faker.readthedocs.io/en/master/).
2. Write them to a csv file.

## Requirements

- [Python 3.11+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

```bash
# Install required python packages via poetry
poetry install

# Activate virtual environment
poetry shell
```

## Usage

```bash
# Activate virtual environment
poetry shell

# Run the script
python main.py
```

Command line help:

```console
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Dummy Excel file generator CLI

Options:
  --help  Show this message and exit.

Commands:
  check  Get excel file's row count
  gen    Generate excel file with random data
```
