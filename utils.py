from os import path
import json
from json.decoder import JSONDecodeError

CONFIG_FILE = 'config.json'

def create_config_file():
    if not path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'x') as file:
            pass

def refine_filename(filename):
    if '.' not in filename:
        filename += '.txt'
    elif not filename.endswith('.txt'):
        filename = filename[:filename.rfind('.')]
        filename += '.txt'
    return filename

def is_book_exist(filename):
    return path.isfile(filename)


def change_default_phonebook(filename):
    create_config_file()
    with open(CONFIG_FILE, 'r') as infile, open(CONFIG_FILE, 'w') as outfile:
        try:
            data = json.load(infile)
        except JSONDecodeError:
            data = {}
        finally:
            data['default-phonebook'] = filename
            json.dump(data, outfile)


def get_default_phonebook():
    with open(CONFIG_FILE, 'r') as conf_file:
        data = json.load(conf_file)
        filename = data['default-phonebook']
    return filename
