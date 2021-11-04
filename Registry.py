import winreg
import os


def get_registry_value(path, name = "", start_key = None):
    
    if isinstance(path, str):
        path = path.split("\\")
    if start_key is None:
        try:
            start_key = getattr(winreg, path[0])
        except AttributeError:
            return "ERROR: INVALID PATH"
        return get_registry_value(path[1:], name, start_key)
    else:
        subkey = path.pop(0)
    try:
        with winreg.OpenKey(start_key, subkey) as handle:
            assert handle, "Cannot open wanted key"
            if path:
                return get_registry_value(path, name, handle)
            else:
                desc, i = None, 0
                try:
                    while not desc or desc[0]!= name:
                        desc = winreg.EnumValue(handle,i)
                        i += 1
                    return desc[1]
                except OSError:
                    return "ERROR: INVALID PATH"
    except FileNotFoundError:
        return "ERROR: INVALID PATH"







