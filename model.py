from __future__ import annotations
from dataclasses import dataclass, fields, asdict
import re
import consts

'''
Regex validators for our model fields
'''
validators: dict[str, str] = {
    consts.FIELD_NAME: r'^([А-Я]?[а-я]+)|([A-Z]?[a-z]+)$',
    consts.FIELD_SECOND_NAME: r'^([А-Я]?[а-я]+)|([A-Z]?[a-z]+)$',
    consts.FIELD_LAST_NAME: r'^([А-Я]?[а-я]+)|([A-Z]?[a-z]+)$',
    consts.FIELD_EMPLOYEE: r'^([А-Я]?[а-я]+)|([A-Z]?[a-z]+)$',
    consts.FIELD_WORK_PHONE: r'^((\+\s?7)|8)\s?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$',
    consts.FIELD_MOBILE_PHONE: r'^((\+\s?7)|8)\s?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$',
}

@dataclass
class PhoneBookEntry:
    '''
    Entry model, containing all fields
    '''
    id: str = ''
    name:str = ''
    second_name: str = ''
    last_name: str = ''
    employee: str = ''
    work_phone: str = ''
    mobile_phone: str = ''
    
    def validate_field(self, field_name:str) -> bool:
        '''
        Validate field according to regex validators
        '''
        field:str = getattr(self, field_name)
        return bool(re.match(validators[field_name], field))

    def get_field_names(self) -> list[str]:
        '''
        Get all field names of our model
        '''
        return [field.name for field in fields(self)]
    
    def get_field_values(self) -> list[str]:
        '''
        Get all field values of our model
        '''
        return asdict(self).values()

    def to_string(self) -> str:
        '''
        Convert instance of our model to a string
        '''
        return consts.TEXTFILE_SEPARATOR.join(asdict(self).values()) + '\n'
    
    def from_string(self, string:str) -> PhoneBookEntry:
        '''
        Get all field values from a string and set instance fields 
        '''
        string:str = string.replace('\n', '')
        fields:list[str] = string.split(consts.TEXTFILE_SEPARATOR)
        for field_name, value in zip(self.get_field_names(), fields):
            setattr(self, field_name, value)
        return self
    

           

