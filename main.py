"""
Python script to generate excel file with fake data
"""
import csv
import click
from faker import Faker
from pathlib import Path
from itertools import islice
from typing import Generator, Iterable

OUTPUT_DIR = Path(__file__).parent / 'output'
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], show_default=True)


def _split_excel(input_file_path: str, max_rows: int) -> int:
    """Split excel file into multiple files"""
    file_name_prefix = input_file_path.split('.')[0]
    file_suffix_num = 0

    with open(input_file_path, "r") as input_file:
        reader = csv.reader(input_file)

        # Use batched to split the data into chunks
        for chunk in _batched(reader, max_rows):
            file_suffix_num += 1
            output_file_path = OUTPUT_DIR / f"{file_name_prefix}_{file_suffix_num}.csv"
            with open(output_file_path, "w", newline='') as output_file:
                writer = csv.writer(output_file)
                writer.writerows(chunk)
    return file_suffix_num


def generate_random_data(rows: int) -> Generator[dict, None, None]:
    """Generate random data"""
    faker = Faker()
    for _ in range(rows):
        yield {
            'file': faker.file_name(),
            'date': faker.date(),
        }


def gen_excel(file_name: str, rows: int):
    """Function to generate excel file with random data"""
    output_path = OUTPUT_DIR / f'{file_name}.csv'
    # Print length of rows+1 because the header rows needs to be counted
    file_info = f"{output_path} with {rows + 1} rows"

    click.echo(click.style(f"[*] Generating {file_info}", fg='yellow'))
    rnd_data = generate_random_data(rows)
    _excel_writer(output_path, rnd_data)
    click.echo(click.style(f"[+] Generated {file_info}", fg='green'))


def _excel_writer(output_path: Path, rnd_data: Generator):
    """Excel writer"""
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['file', 'date'])
        writer.writeheader()
        # Write 100000 rows at a time
        for row in _batched(rnd_data, 100000):
            writer.writerows(row)


def _batched(iterable: Iterable, chunk_size: int) -> tuple:
    """Batched generator"""
    iterator = iter(iterable)
    while chunk := tuple(islice(iterator, chunk_size)):
        yield chunk


def get_excel_row_length(file_path: Path) -> int:
    """Get excel row length"""
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return sum(1 for _ in reader)


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Dummy Excel file generator CLI"""
    # Make sure output folder exists
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir()


@cli.command("gen", no_args_is_help=True)
@click.option('--name', '-n', help="A name for the generated excel file. Ex: test", required=True)
@click.option('--rows', '-r', help='Number of rows', default=2000000)
def gen(name: str, rows: int):
    """Generate excel file with random data"""
    # Generate length of rows-1 because we have a header row
    gen_excel(name, rows - 1)


@cli.command("check", no_args_is_help=True)
@click.argument('file_path', type=click.Path(exists=True), required=True)
def check_excel_length(file_path: Path):
    """Get excel file's row count"""
    result = click.style(get_excel_row_length(file_path), fg='yellow')
    click.echo(click.style(f"[*] {file_path} has {result} rows", fg='yellow'))


@cli.command("split", no_args_is_help=True)
@click.argument('file_path', type=click.Path(exists=True), required=True)
@click.option('--max_rows_per_file', help="Maximum rows per file", default=1048576)
def split_excel_file(file_path: str, max_rows_per_file: int):
    """Split excel file into multiple files which won't exceed row limit"""
    click.echo(click.style(f"[*] Splitting {file_path} into multiple files", fg='yellow'))
    files_count = _split_excel(file_path, max_rows_per_file)
    click.echo(click.style(f"[+] Done splitting {file_path} into {files_count} files", fg='green'))
    click.echo(click.style(f"[*] Check {OUTPUT_DIR}/ for splitted excel files", fg='yellow'))


if __name__ == '__main__':
    cli()
