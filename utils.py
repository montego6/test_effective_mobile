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
    with open(CONFIG_FILE, 'r') as infile:
        try:
            data = json.load(infile)
        except JSONDecodeError:
            data = {}
        finally:
            data['default-phonebook'] = filename
    with open(CONFIG_FILE, 'w') as outfile:
            json.dump(data, outfile)


def get_default_phonebook():
    with open(CONFIG_FILE, 'r') as conf_file:
        try:
            data = json.load(conf_file)
        except JSONDecodeError:
            filename = ''
        else:
            filename = data['default-phonebook']
    return filename


def get_lines_per_page():
    with open(CONFIG_FILE, 'r') as conf_file:
        try:
            data = json.load(conf_file)
        except JSONDecodeError:
            lines_per_page = 5
        else:
            lines_per_page = data['pages-count']
    return lines_per_page