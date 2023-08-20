from os import path

CONFIG_FILE = 'config.json'

def create_config_file():
    if not path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'x') as file:
            pass