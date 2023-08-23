import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated
from typing import List
import os
from model import PhoneBookEntry
from manager import add_entry_to_file, read_all_entries, get_last_id, edit_entries, search_entries, delete_entries
from utils import refine_filename, is_book_exist, change_default_phonebook
from consts import typer_prompts, ALL_FIELD_CHOICES, ChangeFieldChoices, TABLE_HEADER


app = typer.Typer()
console = Console()


@app.command('newbook')
def create_phonebook_command(filename: Annotated[str, typer.Argument()], 
                     set_default: Annotated[bool, typer.Option('--set-default', '-sd')] = False):
    filename = refine_filename(filename)
    try:
        with open(filename, 'x') as file:
            pass
    except FileExistsError:
        rprint('[bold red]Error - this phonebook already exists')
    if set_default:
        change_default_phonebook(filename)


@app.command('rmbook')
def remove_phonebook_command(filename: Annotated[str, typer.Argument()]):
    filename = refine_filename(filename)
    if os.path.exists(filename):
        os.remove(filename)
        rprint('[bold green]Success - phonebook has been deleted')
    else:
        rprint('[bold red]Error - such phonebook doesn''t exist')

@app.command('switch')
def switch_phonebook_command(filename: Annotated[str, typer.Argument()]):
    filename = refine_filename(filename)
    if not is_book_exist(filename):
        rprint('[bold red]Error - this phonebook doesn''t exist')
    else:
        change_default_phonebook(filename)

@app.command('add')
def add_entry_command():
    entry = PhoneBookEntry()
    for field_name in ALL_FIELD_CHOICES:
        setattr(entry, field_name, typer.prompt(typer_prompts[field_name]))
        while not entry.validate_field(field_name):
            rprint('[bold red]Invalid format, try again')
            setattr(entry, field_name, typer.prompt(typer_prompts[field_name]))
    setattr(entry, 'id', str(get_last_id() + 1))
    add_entry_to_file(entry)


@app.command('show')
def show_entries():
    table = Table(*TABLE_HEADER)
    data = read_all_entries()
    for line in data:
        entry = PhoneBookEntry().from_string(line)
        table.add_row(*entry.get_field_values())
    with console.pager():
        console.print(table)


def parse_filter(raw_values):
    result = []
    for raw_value in raw_values:
        field, value = raw_value.split('=')
        if field.strip() not in ALL_FIELD_CHOICES:
            return []
        result.append((field.strip(), value.strip()))
    return result


@app.command('edit')
def edit_entries_command(filters: Annotated[List[str], typer.Option('--filter', '-f', callback=parse_filter)],
                 contains: Annotated[bool, typer.Option('-contains')] = False,
                 eq: Annotated[bool, typer.Option('-eq')] = True,
                 and_option: Annotated[bool, typer.Option('-and')] = True,
                 or_option: Annotated[bool, typer.Option('-or')] = False,
                 field: Annotated[ChangeFieldChoices, typer.Option(case_sensitive=False)] = ChangeFieldChoices.name,
                 ):
    
    if not filters:
        rprint('[bold red]Error - invalid field in filter')
    eq_contains = False if contains else True
    and_or = False if or_option else True
    new_value = typer.prompt(f'Type new value for field {field}')
    rprint(edit_entries(filters, field, new_value, eq_contains, and_or))


@app.command('search')
def search_entries_command(filters: Annotated[List[str], typer.Option('--filter', '-f', callback=parse_filter)],
                 contains: Annotated[bool, typer.Option('-contains')] = False,
                 eq: Annotated[bool, typer.Option('-eq')] = True,
                 and_option: Annotated[bool, typer.Option('-and')] = True,
                 or_option: Annotated[bool, typer.Option('-or')] = False,):

    if not filters:
        rprint('[bold red]Error - invalid field in filter')
    eq_contains = False if contains else True
    and_or = False if or_option else True
    entries = search_entries(filters, eq_contains, and_or)
    table = Table(*TABLE_HEADER)
    for entry in entries:
        table.add_row(*entry.get_field_values())
    with console.pager():
        console.print(table)


@app.command('delete')
def delete_entries_command(filters: Annotated[List[str], typer.Option('--filter', '-f', callback=parse_filter)],
                 contains: Annotated[bool, typer.Option('-contains')] = False,
                 eq: Annotated[bool, typer.Option('-eq')] = True,
                 and_option: Annotated[bool, typer.Option('-and')] = True,
                 or_option: Annotated[bool, typer.Option('-or')] = False,):
    
    if not filters:
        rprint('[bold red]Error - invalid field in filter')
    eq_contains = False if contains else True
    and_or = False if or_option else True
    num_deleted = delete_entries(filters, eq_contains, and_or)
    rprint(f'[bold green]Success - {num_deleted} entries deleted')


if __name__ == '__main__':
    app()