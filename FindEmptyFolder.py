'''Input a path, find any empty folder in it'''
import os
import os.path


def findemptyfolder(path, emptyfolder):
    '''Find empty folder from assigned path, and save the result in emptyfolder list'''
    for root, dirs, files in os.walk(path):
        if len(dirs) + len(files) == 0:
            emptyfolder.append(path.decode('GBK'))
            return
        for subdir in dirs:
            subpath = os.path.join(root, subdir)
            findemptyfolder(subpath, emptyfolder)
        return


PATH = input("input path:\n")
EMPTYFOLDER = []

if os.path.exists(PATH.encode('GBK')) is False:
    pass
else:
    findemptyfolder(PATH.encode('GBK'), EMPTYFOLDER)
    for i in EMPTYFOLDER:
        print("Empty Folder: " + i)
