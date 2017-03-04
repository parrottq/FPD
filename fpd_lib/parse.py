"""
Module used to parse the databases
"""


def parse_update(updates):
    """
    Returns parse package update string

    Keyword arguments:
    updates -- output of "checkupdates" or "pacman -Qu"
    """

    packages = []
    for package in updates.split("\n"):
        arguments = package.split(" ")
        packages.append((arguments[0], arguments[-1]))

    if len(packages) and packages[-1] == ('',''):
        packages = packages[:-1]

    return packages


def extract_db(tar):
    """
    Returns a formated package list of packages for a tar db

    Keyword arguments:
    tar -- tar package database
    """

    database = {}

    for member in tar.getmembers():
        if member.isfile():
            name = member.name

            # Description file
            if name.split("/")[-1] == "desc":
                desc_string = tar.extractfile(name).read().decode()

                values = parse_desc(desc_string)
                name = values["name"]
                del values["name"]

                database[name] = values

    return database


def parse_desc(desc):
    """
    Returns the contents of the desc file

    Keyword arguments:
    desc -- desc file as a string
    """
    package = {}

    # Go thru each value in the desc
    for value in desc.split("\n"*2):
        split_value = value.split("\n")

        # Add the values to a dictionary
        package[split_value[0].strip("%").lower()] = "\n".join(split_value[1:])

    return package
