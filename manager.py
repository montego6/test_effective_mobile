from utils import get_default_phonebook
from model import PhoneBookEntry
from matcher import EntryMatcher
from consts import TEXTFILE_SEPARATOR
import os

phonebook = get_default_phonebook()

def add_entry_to_file(entry:PhoneBookEntry) -> None:
    '''
    Add one entry to the end of a phonebook file
    '''
    with open(phonebook, 'a') as file:
        file.write(entry.to_string())

def get_last_id() -> int:
    '''
    Get id of last entry in a file. If file is empty return 0
    '''
    if not os.path.getsize(phonebook):
        return 0
    with open(phonebook, 'r') as file:
        for line in file:
            pass
        last_line = line
    return int(last_line.split(TEXTFILE_SEPARATOR)[0])

def read_all_entries() -> list[str]:
    '''
    Get all entries from a file
    '''
    with open(phonebook, 'r') as file:
        return file.readlines()

def edit_entries(filters:list[tuple[str, str]], field:str, new_value:str, eq_contains:bool, and_or:bool) -> str:
    '''
    Get all entries from a file, then edit entries that fulfill chosen filters and
    write all entries with changed ones back to file
    Returns string with status of operation
    '''
    raw_entries:list[str] = read_all_entries()
    entries:list[PhoneBookEntry] = [PhoneBookEntry().from_string(raw_entry) for raw_entry in raw_entries]
    num_entries_changed:int = 0
    for entry in entries:
        if EntryMatcher(entry).match(filters, eq_contains, and_or):
            setattr(entry, field, new_value)
            num_entries_changed += 1
            if not entry.validate_field(field):
                return '[bold red]Error - invalid format'
   
    with open(phonebook, 'w') as file:
        file.writelines([entry.to_string() for entry in entries])
    
    return f'[bold green]Success - {num_entries_changed} entries are changed'


def search_entries(filters:list[tuple[str, str]], eq_contains:bool, and_or:bool) -> list[PhoneBookEntry]:
    '''
    Get all entries from file then search for entries that fulfill chosen filters
    Returns list of entries
    '''
    raw_entries:list[str] = read_all_entries()
    all_entries:list[PhoneBookEntry] = [PhoneBookEntry().from_string(raw_entry) for raw_entry in raw_entries]
    return [entry for entry in all_entries if EntryMatcher(entry).match(filters, eq_contains, and_or)]


def delete_entries(filters:list[tuple[str, str]], eq_contains:bool, and_or:bool) -> int:
    '''
    Get all entries from file, then delete entries that fulfill chosen filters 
    and write all entries back to file.
    Returns number of deleted entries
    '''
    raw_entries:list[str] = read_all_entries()
    all_entries:list[PhoneBookEntry] = [PhoneBookEntry().from_string(raw_entry) for raw_entry in raw_entries]
    filtered_entries:list[PhoneBookEntry] = [entry for entry in all_entries if not EntryMatcher(entry).match(filters, eq_contains, and_or)]
    num_deleted_entries:int = len(all_entries) - len(filtered_entries)
    
    with open(phonebook, 'w') as file:
        file.writelines([entry.to_string() for entry in filtered_entries])
    
    return num_deleted_entries



