import os


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
            print("Det var ikke en mulighed. Prøv igen.")


def print_welcome():
    title = """
░█▀▀░█▄█░█▀█░▀▀█░▀█▀░█▀▀░█▀▀░█▀█░░░░█▀▀░█░█░█▀▀
░█▀▀░█░█░█░█░░░█░░█░░█░█░█▀▀░█░█░░░░█▀▀░▄▀▄░█▀▀
░▀▀▀░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀░░▀▀▀░▀░▀░▀▀▀ af barealek

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
