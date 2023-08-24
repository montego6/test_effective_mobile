import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated
from typing import List
import os
from model import PhoneBookEntry
from manager import (
    add_entry_to_file,
    read_all_entries,
    get_last_id,
    edit_entries,
    search_entries,
    delete_entries,
)
from utils import refine_filename, is_book_exist, change_default_phonebook
from consts import typer_prompts, ALL_FIELD_CHOICES, ChangeFieldChoices, TABLE_HEADER


app = typer.Typer()
console = Console()


@app.command("newbook")
def create_phonebook_command(
    filename: Annotated[str, typer.Argument(help="Filename of new phonebook")],
    set_default: Annotated[
        bool, typer.Option("--set-default", "-sd", help="Set new phonebook as default")
    ] = False,
):
    """
    Create new phonebook with a name FILENAME passed as an argument.
    If --set-default option is used, set new phonebook to default phonebook.
    """
    filename: str = refine_filename(filename)
    try:
        with open(filename, "x"):
            pass
    except FileExistsError:
        rprint("[bold red]Error - this phonebook already exists")
    if set_default:
        change_default_phonebook(filename)


@app.command("rmbook")
def remove_phonebook_command(
    filename: Annotated[str, typer.Argument(help="Filename of phonebook to delete")]
):
    """
    Delete phonebook with name FILENAME.
    """
    filename: str = refine_filename(filename)
    if os.path.exists(filename):
        os.remove(filename)
        rprint("[bold green]Success - phonebook has been deleted")
    else:
        rprint("[bold red]Error - such phonebook doesn" "t exist")


@app.command("switch")
def switch_phonebook_command(
    filename: Annotated[str, typer.Argument(help="Filename of a phonebook")]
):
    """
    Set phonebook with name FILENAME as current active phonebook.
    """
    filename: str = refine_filename(filename)
    if not is_book_exist(filename):
        rprint("[bold red]Error - this phonebook doesn" "t exist")
    else:
        change_default_phonebook(filename)


@app.command("add")
def add_entry_command():
    """
    Add entry to current active phonebook. All field values will be interactively prompted,
    and if value wouldn't pass a validation, you would be asked again.
    """
    entry: PhoneBookEntry = PhoneBookEntry()
    for field_name in typer_prompts.keys():
        setattr(entry, field_name, typer.prompt(typer_prompts[field_name]))
        while not entry.validate_field(field_name):
            rprint("[bold red]Invalid format, try again")
            setattr(entry, field_name, typer.prompt(typer_prompts[field_name]))
    setattr(entry, "id", str(get_last_id() + 1))
    add_entry_to_file(entry)


@app.command("show")
def show_entries():
    """
    Show all entries of current active phonebook as a table.
    """
    table: Table = Table(*TABLE_HEADER)
    data: list[str] = read_all_entries()
    for line in data:
        entry: PhoneBookEntry = PhoneBookEntry().from_string(line)
        table.add_row(*entry.get_field_values())
    with console.pager():
        console.print(table)


def parse_filter(raw_values: list[str]) -> list[tuple[str, str]]:
    """
    Parse filters from string in a format field_name=value to list of tuples 
    in a format [(field_name, value)]
    If field_name is invalid, returns empty list
    """
    result: list[tuple[str, str]] = []
    for raw_value in raw_values:
        field, value = raw_value.split("=")
        if field.strip() not in ALL_FIELD_CHOICES:
            return []
        result.append((field.strip(), value.strip()))
    return result


@app.command("edit")
def edit_entries_command(
    filters: Annotated[
        List[str],
        typer.Option(
            "--filter",
            "-f",
            callback=parse_filter,
            help="Filters in a format field_name=value",
        ),
    ],
    contains: Annotated[
        bool,
        typer.Option(
            "-contains", help="Filters will check if field value contains filter value"
        ),
    ] = False,
    eq: Annotated[
        bool,
        typer.Option(
            "-eq", help="Filters will check if field value is equal to filter value"
        ),
    ] = True,
    and_option: Annotated[
        bool, typer.Option("-and", help="Multiple filters are grouped as logical AND")
    ] = True,
    or_option: Annotated[
        bool, typer.Option("-or", help="Multiple filters are grouped as logical OR")
    ] = False,
    field: Annotated[
        ChangeFieldChoices, typer.Option(case_sensitive=False)
    ] = ChangeFieldChoices.name.value,
):
    """
    Edit entries that fulfill the chosen filters. Filters are set with -f option and 
    should be in a format "field_name=value". Possible field names are: 
    id, name, second_name, last_name, employee, work_phone, mobile_phone.
    By default -eq option is set and filters are checking for equality of values. 
    If -contains option is set, then filters are checking for containment of filter value. 
    Also by default -and option is set and filters are grouped by logical AND, 
    but you can set -or option to group by logical OR. Also you should set
    --field option containing field name, which you want to change. Change value will be prompted.
    """
    if not filters:
        rprint("[bold red]Error - invalid field in filter")
    eq_contains: bool = False if contains else True
    and_or: bool = False if or_option else True
    new_value: str = typer.prompt(f"Type new value for field {field}")
    rprint(edit_entries(filters, field, new_value, eq_contains, and_or))


@app.command("search")
def search_entries_command(
    filters: Annotated[
        List[str],
        typer.Option(
            "--filter",
            "-f",
            callback=parse_filter,
            help="Filters in a format field_name=value",
        ),
    ],
    contains: Annotated[
        bool,
        typer.Option(
            "-contains", help="Filters will check if field value contains filter value"
        ),
    ] = False,
    eq: Annotated[
        bool,
        typer.Option(
            "-eq", help="Filters will check if field value is equal to filter value"
        ),
    ] = True,
    and_option: Annotated[
        bool, typer.Option("-and", help="Multiple filters are grouped as logical AND")
    ] = True,
    or_option: Annotated[
        bool, typer.Option("-or", help="Multiple filters are grouped as logical OR")
    ] = False,
):
    """
    Search entries that fulfill the chosen filters and show them as a table.
    Filters are set with -f option and should be in a format
    "field_name=value". Possible field names are: 
    id, name, second_name, last_name, employee, work_phone, mobile_phone.
    By default -eq option is set and filters are checking for equality of values. 
    If -contains option is set, then filters are checking for containment of filter value. 
    Also by default -and option is set and filters are grouped by logical AND, 
    but you can set -or option to group by logical OR.
    """
    if not filters:
        rprint("[bold red]Error - invalid field in filter")
    eq_contains: bool = False if contains else True
    and_or: bool = False if or_option else True
    entries: list[PhoneBookEntry] = search_entries(filters, eq_contains, and_or)
    table: Table = Table(*TABLE_HEADER)
    for entry in entries:
        table.add_row(*entry.get_field_values())
    with console.pager():
        console.print(table)


@app.command("delete")
def delete_entries_command(
    filters: Annotated[
        List[str],
        typer.Option(
            "--filter",
            "-f",
            callback=parse_filter,
            help="Filters in a format field_name=value",
        ),
    ],
    contains: Annotated[
        bool,
        typer.Option(
            "-contains", help="Filters will check if field value contains filter value"
        ),
    ] = False,
    eq: Annotated[
        bool,
        typer.Option(
            "-eq", help="Filters will check if field value is equal to filter value"
        ),
    ] = True,
    and_option: Annotated[
        bool, typer.Option("-and", help="Multiple filters are grouped as logical AND")
    ] = True,
    or_option: Annotated[
        bool, typer.Option("-or", help="Multiple filters are grouped as logical OR")
    ] = False,
):
    """
    Delete entries that fulfill the chosen filters. Filters are set with -f option 
    and should be in a format "field_name=value". Possible field names are: 
    id, name, second_name, last_name, employee, work_phone, mobile_phone.
    By default -eq option is set and filters are checking for equality of values. 
    If -contains option is set, then filters are checking for containment of filter value. 
    Also by default -and option is set and filters are grouped by logical AND, 
    but you can set -or option to group by logical OR.
    """
    if not filters:
        rprint("[bold red]Error - invalid field in filter")
    eq_contains: bool = False if contains else True
    and_or: bool = False if or_option else True
    num_deleted: int = delete_entries(filters, eq_contains, and_or)
    rprint(f"[bold green]Success - {num_deleted} entries deleted")


if __name__ == "__main__":
    app()
