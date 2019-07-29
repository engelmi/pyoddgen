import shutil
from os import makedirs
from os.path import exists, isfile, isdir


def create_directory(directory):
    if not exists(directory):
        makedirs(directory)
        return True
    return False


def create_directories(directory_list):
    try:
        for directory in directory_list:
            create_directory(directory)
    except Exception as ex:
        return False, ex
    return True, None


def delete_directory(directory, force=False):
    if exists(directory) and force:
        shutil.rmtree(directory, ignore_errors=True)
        return True
    return False


def delete_directories(directory_list):
    try:
        for directory in directory_list:
            delete_directory(directory)
    except Exception as ex:
        return False, ex
    return True, None
