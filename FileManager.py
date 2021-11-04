import os

def view_folder(path):
    # list of tuple (path, is this a direction)
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

#print(view_folder("C:\\"))
