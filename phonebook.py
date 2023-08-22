import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated
from enum import Enum
from model import PhoneBookEntry
from manager import add_entry_to_file, read_all_entries, get_last_id, edit_entries
from utils import refine_filename, is_book_exist, change_default_phonebook, get_lines_per_page
import config_commands


app = typer.Typer()
app.add_typer(config_commands.app, name='config')
console = Console()

typer_prompts = {
        'name': 'Type first name',
        'second_name': 'Type second name',
        'last_name': 'Type last name',
        'employee': 'Type organization name',
        'work_phone': 'Type work phone',
        'mobile_phone': 'Type mobile phone',
    }

class ChangeFieldChoices(str, Enum):
    name:str = 'name'
    second_name: str = 'second_name'
    last_name: str = 'last_name'
    employee: str = 'employee'
    work_phone: str = 'work_phone'
    mobile_phone: str = 'mobile_phone'

class SearchFieldChoices(str, Enum):
    id: str = 'id'
    name:str = 'name'
    second_name: str = 'second_name'
    last_name: str = 'last_name'
    employee: str = 'employee'
    work_phone: str = 'work_phone'
    mobile_phone: str = 'mobile_phone'


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
    for field_name in typer_prompts.keys():
        setattr(entry, field_name, typer.prompt(typer_prompts[field_name]))
        while not entry.validate_field(field_name):
            rprint('[bold red]Invalid format')
            setattr(entry, field_name, typer.prompt(typer_prompts[field_name]))
        setattr(entry, 'id', str(get_last_id() + 1))
    add_entry_to_file(entry.to_string())


@app.command('show')
def show_entries():
    table = Table('id', 'First name', 'Second name', 'Last name', 'Organisation', 'Work phone', 'Mobile phone')
    data = read_all_entries()
    for line in data:
        entry = PhoneBookEntry()
        entry = entry.from_string(line)
        table.add_row(*entry.get_field_values())
    with console.pager():
        console.print(table)

@app.command('edit')
def edit_entries_command(search_value: Annotated[str, typer.Option()],
                 search_field: Annotated[SearchFieldChoices, typer.Option()] = SearchFieldChoices.id,
                 contains: Annotated[bool, typer.Option()] = False,
                 eq: Annotated[bool, typer.Option()] = True,
                 field: Annotated[ChangeFieldChoices, typer.Option(case_sensitive=False)] = ChangeFieldChoices.name,
                 ):
    new_value = typer.prompt('Type new value for field')
    edit_entries(search_field, search_value, field, new_value)

@app.command()
def main(name: str):
    print(f'Hello {name}')


if __name__ == '__main__':
    app()