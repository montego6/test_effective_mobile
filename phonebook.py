import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated
from model import PhoneBookEntry
from manager import add_entry_to_file, count_entry_lines, read_all_entries
from utils import CONFIG_FILE, refine_filename, is_book_exist, change_default_phonebook

app = typer.Typer()
console = Console()


@app.command('newbook')
def create_phonebook(filename: Annotated[str, typer.Argument()], 
                     set_default: Annotated[bool, typer.Option('--set-default', '-sd')] = False):
    filename = refine_filename(filename)
    
    try:
        with open(filename, 'x') as file:
            pass
    except FileExistsError:
        rprint('[bold red]This phonebook already exists')
    
    if set_default:
        change_default_phonebook(filename)


@app.command('switch')
def switch_phonebook(filename: Annotated[str, typer.Argument()]):
    filename = refine_filename(filename)
    if not is_book_exist(filename):
        rprint('[bold red]This phonebook doesn''t exist')
    else:
        change_default_phonebook(filename)

@app.command('add')
def add_entry():
    entry = PhoneBookEntry()
    for field_name in entry.get_field_names():
        setattr(entry, field_name, typer.prompt(entry.typer_prompts[field_name]))
        while not entry.validate_field(field_name):
            rprint('[bold red]Invalid format')
            setattr(entry, field_name, typer.prompt(entry.typer_prompts[field_name]))
    add_entry_to_file(count_entry_lines() + 1, entry.to_string())


@app.command('show')
def show_entries():
    table = Table('id', 'First name', 'Second name', 'Last name', 'Organisation', 'Work phone', 'Mobile phone')
    data = read_all_entries()
    print(data)
    for line in data:
        entry = PhoneBookEntry()
        id = entry.from_string(line)
        table.add_row(id, *entry.get_field_values())
    console.print(table)


@app.command()
def main(name: str):
    print(f'Hello {name}')


if __name__ == '__main__':
    app()