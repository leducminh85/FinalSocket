import os
import string
from ctypes import windll

def view_folder(path):
    try:
        if not os.path.isdir(path):
            list_dir = []
        else:
            list_dir = [(x, os.path.isdir(os.path.join(path, x)))
                        for x in os.listdir(path)]
        list_dir.sort(key = lambda x : not x[1])
        return list_dir
    except Exception:
        return []



def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

