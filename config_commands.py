import typer
from typing_extensions import Annotated
import json
from utils import CONFIG_FILE

app = typer.Typer()


@app.command('set-pages')
def set_pages_config(page_count: Annotated[int, typer.Argument()]):
    with open(CONFIG_FILE, 'r') as file:
        data = json.load(file)
        data['pages-count'] = page_count
    with open(CONFIG_FILE, 'w') as file:
        json.dump(data, file)
