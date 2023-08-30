from fuzzyfinder import fuzzyfinder

import os
import sys
import string
from msvcrt import getch
from time import sleep
from shutil import get_terminal_size


def get_dict_option_from_user(options: dict):
    # Generate options

    for i, option in enumerate(options):
        print(f"{i + 1}: {option.title()}")

    while True:
        candidate = input("> ")
        if candidate.lower() in options:
            return candidate.lower(), options.get(candidate.lower())
        try:
            selected = int(candidate)
            return candidate.lower(), list(options.values())[selected - 1]
        except (ValueError, IndexError):
            print("That wasn't an option. Try again!")


def fuzzyfind_value_from_list(options: list[str, ...]) -> str:
    """
    Brug fuzzyfinder til at finde en værdi fra en liste.
    Funktionen er blokerende indtil der er fundet en værdi.

    Lavet af Alek

    :param options: Den liste du vil søge i, og få en værdi tilbage fra.
    :return: Den værdi der blev valgt.
    """
    def _reset_line():
        print(" " * get_terminal_size().columns, end="\r")

    def _print():
        _reset_line()
        _results = ', '.join(_fuzzyquery(search_query, options))
        if len(_results) > 32:
            _results = _results[:29] + "..."
        print(f" > {search_query:<8} | {_results}", end="\r")

    def _fuzzyquery(term: str, selection: list):
        return list(fuzzyfinder(term, selection))

    search_query = ""
    _print()
    while True:
        key = getch()
        if key in (b"\x1b", b"\x03"):  # Hvis man klikker CTRL + C eller ESCAPE
            _reset_line()
            print("Escape was pressed. Exiting...")
            sleep(2)
            return sys.exit()

        if key == b"\r":  # Enter

            if search_query in options:
                _reset_line()
                return search_query

            result_candidates = _fuzzyquery(search_query, options)
            if len(result_candidates) == 1:
                _reset_line()
                return result_candidates[0]

        if key == b"\x08":  # Backspace
            search_query = search_query[:-1]
            _print()
            continue

        if len(search_query) == 8:
            continue

        try:
            character = key.decode('utf-8')
        except UnicodeDecodeError:
            _map = {b'\x91': 'æ', b'\x9b': 'ø', b'\x86': 'å'}
            character = _map.get(key, '')

        if character in string.ascii_letters + 'æøå':
            search_query += character

        _print()


def print_welcome():
    title = """
░█▀▀░█▄█░█▀█░▀▀█░▀█▀░█▀▀░█▀▀░█▀█░░░░█▀▀░█░█░█▀▀
░█▀▀░█░█░█░█░░░█░░█░░█░█░█▀▀░█░█░░░░█▀▀░▄▀▄░█▀▀
░▀▀▀░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░░▀▀▀░▀░▀░▀▀▀ by barealek

"""
    print(title)
    return


def ensure_dir(dir_name):
    """
        Makes sure that the specified directory exists. If it doesn't, it will be created.
        :param dir_name: The directory to make sure exists
        :return: None
        """
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
