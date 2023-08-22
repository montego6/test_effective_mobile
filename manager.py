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
    
def get_last_id():
    with open(phonebook, 'r') as file:
        for line in file:
            pass
        last_line = line
    return int(last_line.split('|')[0])

def read_all_entries():
    with open(phonebook, 'r') as file:
        return file.readlines()