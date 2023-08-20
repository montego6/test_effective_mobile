from os import path
from utils import get_default_phonebook


def add_entry_to_file(entry):
    phonebook = get_default_phonebook()
    with open(phonebook, 'a') as file:
        file.write(entry)