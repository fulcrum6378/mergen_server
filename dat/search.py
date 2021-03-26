from os import listdir
from os.path import isfile, join
import dat.config as cfg


def folders(path):
    files = listdir(path)
    arr = []
    for f in files:
        if not isfile(join(path, f)) and f not in cfg.default_folders:
            arr.append(f)
    return arr


def object(name):
    found = []
    found = object_folder(name, cfg.root + "object", found)
    return found


def object_folder(name, path, found):
    all = folders(path)
    for f in all:
        if f == name: found.append(path + "/" + f)
        found = object_folder(name, path + "/" + f, found)
    return found
