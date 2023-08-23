import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated
from typing import List, Tuple
from enum import Enum
from model import PhoneBookEntry
from manager import add_entry_to_file, read_all_entries, get_last_id, edit_entries, search_entries
from utils import refine_filename, is_book_exist, change_default_phonebook
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

filter_choices = [field.value for field in SearchFieldChoices]


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
        entry = PhoneBookEntry().from_string(line)
        table.add_row(*entry.get_field_values())
    with console.pager():
        console.print(table)

def parse_filter(raw_values):
    result = []
    for raw_value in raw_values:
        field, value = raw_value.split('=')
        if field.strip() not in filter_choices:
            return []
        result.append((field.strip(), value.strip()))
    return result


@app.command('edit')
def edit_entries_command(filters: Annotated[List[str], typer.Option('--filter', '-f', callback=parse_filter)],
                 contains: Annotated[bool, typer.Option()] = False,
                 eq: Annotated[bool, typer.Option()] = True,
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
                 contains: Annotated[bool, typer.Option()] = False,
                 eq: Annotated[bool, typer.Option()] = True,
                 and_option: Annotated[bool, typer.Option('-and')] = True,
                 or_option: Annotated[bool, typer.Option('-or')] = False,):

    if not filters:
        rprint('[bold red]Error - invalid field in filter')
    eq_contains = False if contains else True
    and_or = False if or_option else True
    entries = search_entries(filters, eq_contains, and_or)
    table = Table('id', 'First name', 'Second name', 'Last name', 'Organisation', 'Work phone', 'Mobile phone')
    for entry in entries:
        table.add_row(*entry.get_field_values())
    with console.pager():
        console.print(table)



if __name__ == '__main__':
    app()