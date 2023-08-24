from os import path
import json
from json.decoder import JSONDecodeError

CONFIG_FILE = "config.json"


def create_config_file() -> None:
    """
    Create config file if it doesn't exist
    """
    if not path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "x"):
            pass


def refine_filename(filename: str) -> str:
    """
    Refines filename in a way that filename will be name.txt
    """
    if "." not in filename:
        filename += ".txt"
    elif not filename.endswith(".txt"):
        filename = filename[: filename.rfind(".")]
        filename += ".txt"
    return filename


def is_book_exist(filename: str) -> bool:
    """
    Check if phonebook exist
    """
    return path.isfile(filename)


def change_default_phonebook(filename: str) -> None:
    """
    Changes current active phonebook in config file
    """
    create_config_file()
    with open(CONFIG_FILE, "r") as infile:
        try:
            data: dict[str, str] = json.load(infile)
        except JSONDecodeError:
            data = {}
        finally:
            data["default-phonebook"] = filename
    with open(CONFIG_FILE, "w") as outfile:
        json.dump(data, outfile)


def get_default_phonebook() -> str:
    """
    Gets current active phonebook from config file
    """
    with open(CONFIG_FILE, "r") as conf_file:
        try:
            data: dict[str, str] = json.load(conf_file)
        except JSONDecodeError:
            filename: str = ""
        else:
            filename = data["default-phonebook"]
    return filename
