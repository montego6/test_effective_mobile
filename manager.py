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

def edit_entries(filters, field, new_value, eq_contains, and_or):
    raw_entries = read_all_entries()
    entries = [PhoneBookEntry().from_string(raw_entry) for raw_entry in raw_entries]
    num_entries_changed = 0
    for entry in entries:
        if entry.match(filters, eq_contains, and_or):
            setattr(entry, field, new_value)
            num_entries_changed += 1
            if not entry.validate_field(field):
                return '[bold red]Error - invalid format'
   
    with open(phonebook, 'w') as file:
        file.writelines([entry.to_string() for entry in entries])
    
    return f'[bold green]Success - {num_entries_changed} entries are changed'


def search_entries(filters, eq_contains, and_or):
    raw_entries = read_all_entries()
    all_entries = [PhoneBookEntry().from_string(raw_entry) for raw_entry in raw_entries]
    result = []
    return [entry for entry in all_entries if entry.match(filters, eq_contains, and_or)]