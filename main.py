"""
Python script to generate random excel file
"""
import csv
import click
from faker import Faker
from typing import List
from pathlib import Path
from io import TextIOWrapper

OUTPUT_PATH = Path(__file__).parent / 'output'


class ExcelSplitter():
    def __init__(self, input_file_path: str, max_rows: int = 100000):
        self.input_file_path: str = input_file_path
        self.max_rows: int = max_rows
        self.file_handler: TextIOWrapper = None
        self.writer: csv.writer = None
        self.row_count = 0
        self.file_suffix_num = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_handler.close()

    def split(self):
        """
        Split excel file into multiple files
        """
        file_name_prefix = self.input_file_path.split('.')[0]

        with open(self.input_file_path, "r") as input_file:
            reader = csv.reader(input_file)
            row_count: int = 0
            file_suffix_num: int = 0

            for row in reader:
                # If the counter is equal to 0, create a new output file
                if row_count == 0:
                    file_suffix_num += 1
                    output_file_path = OUTPUT_PATH / f"{file_name_prefix}_{file_suffix_num}.csv"
                    self.file_handler = open(output_file_path, "w", newline='')
                    self.writer = csv.writer(self.file_handler)

                # If the counter is not equal to 0, write the row to the existing output file
                self.writer.writerow(row)
                row_count += 1

                if row_count == self.max_rows:
                    self.file_handler.close()
                    row_count = 0


def generate_random_data(rows: int) -> List[dict]:
    """
    Generate random data
    """
    faker = Faker()
    return [
        {
            'file': faker.file_name(),
            'date': faker.date(),
        }
        for _ in range(rows)
    ]


def gen_excel(file_name: str, rows: int):
    """
    Function to generate excel file with random data
    """
    file_name = f'{file_name}.csv'
    click.echo(click.style(f"[*] Generating {file_name} with {rows} rows", fg='yellow'))
    rnd_data = generate_random_data(rows)
    with open(OUTPUT_PATH / file_name, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rnd_data[0].keys())
        writer.writeheader()
        writer.writerows(rnd_data)
    click.echo(click.style(f"[+] Generated {file_name} with {rows} rows", fg='green'))


def get_excel_row_length(file_path: Path) -> int:
    """
    Get excel row length
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return sum(1 for _ in reader)


@click.group(context_settings=dict(show_default=True))
def cli():
    """
    Dummy Excel file generator CLI
    """
    # Check if output folder exists
    if not OUTPUT_PATH.exists():
        OUTPUT_PATH.mkdir()


@cli.command()
@click.option('--file_name', '-f', help='File name', required=True)
@click.option('--rows', '-r', help='Number of rows', default=2000000)
def gen(file_name: str, rows: int):
    """
    Generate excel file with random data
    """
    gen_excel(file_name, rows)


@cli.command("check")
@click.option('--file_path', '-f', help='File path', required=True)
def check_excel_length(file_path: Path):
    """
    Get excel file's row count
    """
    result = click.style(get_excel_row_length(file_path), fg='yellow')
    click.echo(click.style(f"[*] {file_path} has {result} rows", fg='yellow'))


@cli.command("split")
@click.option('--file_path', '-f', help='File path', required=True)
@click.option('--max_rows_per_file', '-m', help='Max rows per file', default=1000000)
def split_excel_file(file_path: str, max_rows_per_file: int):
    """
    Split excel file into multiple files which won't exceed row limit
    """
    click.echo(click.style(f"[*] Splitting {file_path} into multiple files", fg='yellow'))
    with ExcelSplitter(file_path, max_rows_per_file) as splitter:
        splitter.split()
    click.echo(click.style(f"[+] Done splitting {file_path} into multiple files", fg='green'))
    click.echo(click.style(f"[*] Check {OUTPUT_PATH} for splitted files", fg='yellow'))


if __name__ == '__main__':
    cli()
