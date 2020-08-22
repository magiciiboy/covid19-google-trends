import os

def mkdir_if_not_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path