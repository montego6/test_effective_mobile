import typer
from rich import print as rprint
import json
from json.decoder import JSONDecodeError
from typing_extensions import Annotated
from pathlib import Path
from utils import create_config_file, CONFIG_FILE

app = typer.Typer()


@app.command('newbook')
def create_phonebook(filename: Annotated[str, typer.Argument()], 
                     set_default: Annotated[bool, typer.Option('--set-default', '-sd')] = False):
    try:
        with open(filename, 'x') as file:
            pass
    except FileExistsError:
        rprint('[bold red]This phonebook already exists')
    
    if set_default:
        create_config_file()
        with open(CONFIG_FILE, 'r') as infile, open(CONFIG_FILE, 'w') as outfile:
            try:
                data = json.load(infile)
            except JSONDecodeError:
                data = {}
            finally:
                data['default-phonebook'] = filename
                json.dump(data, outfile)
        
        
        # with open('confing.json', 'r') as file:
        #     raw_data = file.read()
        #     json_data = json.loads(raw_data)
        #     json_data['default-phonebook'] = filename
        # with open('confing.json', 'w') as file:
        #     file.write(json.dumps(json_data))



@app.command()
def main(name: str):
    print(f'Hello {name}')


if __name__ == '__main__':
    app()