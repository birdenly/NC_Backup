import math
import os
import time
import zipfile


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def get_size(path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size
try:
    currentUser = os.path.expanduser('~')
    ncAppdataPath = os.path.join(currentUser,"NucleusCoop")
    savePathOutput = os.path.join(os.getcwd(),"backup") 
    
    if os.path.exists(ncAppdataPath):
        print("Nucleus Appdata folder found!")
        size = convert_size(get_size(ncAppdataPath))
        print(f"Nucleus Appdata path: {ncAppdataPath}")
        print(f"Folder size:  {size}")
        accept = input("Do you want to backup this folder? (y/n): ")
        if accept.lower() == 'y':
            print("Backing up...")
            if os.path.exists(savePathOutput + ".zip"):
                os.remove(savePathOutput + ".zip")
                print("Old backup removed.")
                
            with zipfile.ZipFile(savePathOutput + ".zip", "w", strict_timestamps=False) as zf:
                for dirpath, dirnames, filenames in os.walk(ncAppdataPath):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        zf.write(fp, os.path.relpath(fp, ncAppdataPath))
            print(f"Backup created at {savePathOutput}.zip")
    else:
        print("Nucleus Appdata folder not found!")
        print(f"Expected path: {ncAppdataPath}. If this doesnt exist, you may have no handlers that saves in this path.")
        
except Exception as e:
    print(f"GENERAL ERROR: {e}")