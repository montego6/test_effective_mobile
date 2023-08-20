from dataclasses import dataclass, fields, asdict
import typing
import re

@dataclass
class PhoneBookEntry:
    name:str = ''
    second_name: str = ''
    last_name: str = ''
    employee: str = ''
    work_phone: str = ''
    mobile_phone: str = ''
    
    validators: typing.ClassVar = {
        'name': r'^([А-Я]?[а-я]+)|([A-Z]?[a-z]+)$',
        'second_name': r'^([А-Я]?[а-я]+)|([A-Z]?[a-z]+)$',
        'last_name': r'^([А-Я]?[а-я]+)|([A-Z]?[a-z]+)$',
        'employee': r'^([А-Я]?[а-я]+)|([A-Z]?[a-z]+)$',
        'work_phone': r'^((\+\s?7)|8)\s?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$',
        'mobile_phone': r'^((\+\s?7)|8)\s?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$',
    }

    typer_prompts: typing.ClassVar = {
        'name': 'Type first name',
        'second_name': 'Type second name',
        'last_name': 'Type last name',
        'employee': 'Type organization name',
        'work_phone': 'Type work phone',
        'mobile_phone': 'Type mobile phone',

    }

    def validate_field(self, field_name):
        field = getattr(self, field_name)
        print(re.match(self.validators[field_name], field))
        return bool(re.match(self.validators[field_name], field))

    def get_field_names(self):
        return [field.name for field in fields(self)]
    
    def get_field_values(self):
        return asdict(self).values()

    def to_string(self):
        return '|'.join(asdict(self).values()) + '\n'
    
    def from_string(self, string):
        string = string.replace('\n', '')
        fields = string.split('|')
        id = fields[0]
        del fields[0]
        for field_name, value in zip(self.get_field_names(), fields):
            setattr(self, field_name, value)
        return id

