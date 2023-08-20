import typer
from rich import print as rprint
from typing_extensions import Annotated
from model import PhoneBookEntry
from manager import add_entry_to_file 
from utils import CONFIG_FILE, refine_filename, is_book_exist, change_default_phonebook

app = typer.Typer()


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
    add_entry_to_file(entry.to_string())

@app.command()
def main(name: str):
    print(f'Hello {name}')


if __name__ == '__main__':
    app()