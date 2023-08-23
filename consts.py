from enum import Enum

FIELD_ID = 'id'
FIELD_NAME = 'name'
FIELD_SECOND_NAME = 'second_name'
FIELD_LAST_NAME = 'last_name'
FIELD_EMPLOYEE = 'employee'
FIELD_WORK_PHONE = 'work_phone'
FIELD_MOBILE_PHONE = 'mobile_phone'

ALL_FIELD_CHOICES = (FIELD_ID, FIELD_NAME, FIELD_SECOND_NAME, FIELD_LAST_NAME, FIELD_EMPLOYEE, FIELD_WORK_PHONE, FIELD_MOBILE_PHONE)

TABLE_HEADER = ('id', 'First name', 'Second name', 'Last name', 'Organisation', 'Work phone', 'Mobile phone')

TEXTFILE_SEPARATOR = '|'

typer_prompts = {
        FIELD_NAME: 'Type first name',
        FIELD_SECOND_NAME: 'Type second name',
        FIELD_LAST_NAME: 'Type last name',
        FIELD_EMPLOYEE: 'Type organization name',
        FIELD_WORK_PHONE: 'Type work phone',
        FIELD_MOBILE_PHONE: 'Type mobile phone',
    }

class ChangeFieldChoices(str, Enum):
    name:str = FIELD_NAME
    second_name: str = FIELD_SECOND_NAME
    last_name: str = FIELD_LAST_NAME
    employee: str = FIELD_EMPLOYEE
    work_phone: str = FIELD_WORK_PHONE
    mobile_phone: str = FIELD_MOBILE_PHONE

