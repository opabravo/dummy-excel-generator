"""
Python script to generate random excel file
"""
import csv
import click
from faker import Faker
from typing import List
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent / 'output'


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


if __name__ == '__main__':
    cli()
