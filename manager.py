from os import path
from utils import get_default_phonebook

phonebook = get_default_phonebook()

def add_entry_to_file(id, entry):
    phonebook = get_default_phonebook()
    with open(phonebook, 'a') as file:
        file.write(str(id) + '|' + entry)

def count_entry_lines():
    phonebook = get_default_phonebook()
    with open(phonebook, 'rbU') as file:
        return sum(1 for _ in file)

def read_all_entries():
    with open(phonebook, 'r') as file:
        return file.readlines()