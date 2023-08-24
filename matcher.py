from model import PhoneBookEntry
from typing import Callable

class EntryMatcher:
    '''
    Class for matching entries to chosen filters
    '''
    
    def __init__(self, entry:PhoneBookEntry) -> None:
        self.entry = entry

    def match(self, filters:list[tuple[str, str]], eq_contains:bool, and_or:bool) -> Callable[[list[tuple[str, str]], bool], bool]:
        '''
        Main match function that delegates to other funcs
        according to selected eq or contains option
        '''
        if eq_contains:
            return self.eqmatch(filters, and_or)
        else:
            return self.containsmatch(filters, and_or)

    def eqmatch(self, filters:list[tuple[str, str]], and_or:bool) -> bool:
        '''
        Matching for equality with AND or OR logic
        '''
        matched:bool = False
        for field, value in filters:
            if and_or:
                matched = True
                if getattr(self.entry, field) != value:
                    matched = False
                    break
            else:
                if getattr(self.entry, field) == value:
                    matched = True
                    break
        return matched    
            
    def containsmatch(self, filters:list[tuple[str, str]], and_or:bool) -> bool:
        '''
        Matching for containment with AND or OR logic
        '''
        matched:bool = False
        for field, value in filters:          
            if and_or:
                matched = True
                if getattr(self.entry, field).find(value) == -1:
                    matched = False
                    break
            else:
                if getattr(self.entry, field).find(value) != -1:
                    matched = True 
                    break
        return matched