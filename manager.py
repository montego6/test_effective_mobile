from os import path
from utils import get_default_phonebook
from model import PhoneBookEntry

phonebook = get_default_phonebook()

def add_entry_to_file(entry):
    with open(phonebook, 'a') as file:
        file.write(entry)

def get_last_id():
    with open(phonebook, 'r') as file:
        for line in file:
            pass
        last_line = line
    return int(last_line.split('|')[0])

def read_all_entries():
    with open(phonebook, 'r') as file:
        return file.readlines()

def edit_entries(search_field, search_value, field, new_value, eq=True, contains=False):
    raw_entries = read_all_entries()
    entries = [PhoneBookEntry().from_string(raw_entry) for raw_entry in raw_entries]
    for entry in entries:
        if entry.match(search_field, search_value, eq, contains):
            setattr(entry, field, new_value)

    with open(phonebook, 'w') as file:
        file.writelines([entry.to_string() for entry in entries])