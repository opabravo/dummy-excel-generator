# dummy-excel-tools

This is a tool pack to generate, split and check Excel files with random data.

![](https://i.imgur.com/J7MdeJY.png)

# Features

- [x] Generate Excel files with random data which can exceed the row limit of `1048576`.
- [x] Split Excel files into multiple files which won't exceed row limit.
- [x] Check Excel file's row count.

## Description

The generated Excel files can be used to test the condition when row count exceed the limit of `1048576`, so it won't be able to open.

In our case, we were testing against **OPSWAT**'s CDR (Content Disarm and Reconstruction) technology, which can detect and reconstruct malicious data.

## Requirements

- [Python 3.11+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

```bash
# Clone the repo
git clone https://github.com/opabravo/dummy-excel-tools
cd dummy-excel-tools

# Install required python packages via poetry
poetry install
```

PS: Not using `pandas` to split the csv file because `csv` is lighter and faster for the purpose.

## Usage

```bash
# Activate virtual environment
poetry shell

# Run the script
python main.py
```

### Command line help

```console
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Dummy Excel file tools CLI

Options:
  --help  Show this message and exit.

Commands:
  check  Get excel file's row count
  gen    Generate excel file with random data
  split  Split excel file into multiple files which won't exceed row limit

```

## License

[MIT](LICENSE)

