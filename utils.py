import math
import os
import time
import zipfile

OUTPUT = os.path.join(os.getcwd(),"backup") 

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

def ncEnvBackup(path):
    print("Backing up...")
    if os.path.exists(OUTPUT + ".zip"):
        os.remove(OUTPUT + ".zip")
        print("Old backup removed.")
        
    with zipfile.ZipFile(OUTPUT + ".zip", "w", strict_timestamps=False) as zf:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                zf.write(fp, os.path.relpath(fp, path))
    print(f"Backup created at {OUTPUT}.zip")

        
def ncMainBackup(path):
    size = convert_size(get_size(path))
    print(f"Nucleus main folder path: {path}")
    print(f"Folder size:  {size}")
    accept = input("Do you want to backup Nucleus Enviromment folder? (y/n): ")
    if accept.lower() == 'y':
        print("Backing up...")
        if os.path.exists(OUTPUT + ".zip"):
            os.remove(OUTPUT + ".zip")
            print("Old backup removed.")
            
        with zipfile.ZipFile(OUTPUT + ".zip", "w", strict_timestamps=False) as zf:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    zf.write(fp, os.path.relpath(fp, path))
        print(f"Backup created at {OUTPUT}.zip")