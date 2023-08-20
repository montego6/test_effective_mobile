import typer
from rich import print as rprint
from typing_extensions import Annotated
from pathlib import Path
from utils import create_config_file, CONFIG_FILE, refine_filename, is_book_exist, change_default_phonebook

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
    name = typer.prompt('Type first name')
    second_name = typer.prompt('Type second name')
    last_name = typer.prompt('Type last name')
    employee = typer.prompt('Type name of your organization')
    work_phone = typer.prompt('Type work phone number')
    mobile_phone = typer.prompt('Type your mobile phone number')


@app.command()
def main(name: str):
    print(f'Hello {name}')


if __name__ == '__main__':
    app()