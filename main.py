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

def ncEnvBackup(path):
    print("Backing up...")
    if os.path.exists(savePathOutput + ".zip"):
        os.remove(savePathOutput + ".zip")
        print("Old backup removed.")
        
    with zipfile.ZipFile(savePathOutput + ".zip", "w", strict_timestamps=False) as zf:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                zf.write(fp, os.path.relpath(fp, path))
    print(f"Backup created at {savePathOutput}.zip")

        
def ncMainBackup(path):
    size = convert_size(get_size(path))
    print(f"Nucleus main folder path: {path}")
    print(f"Folder size:  {size}")
    accept = input("Do you want to backup Nucleus Enviromment folder? (y/n): ")
    if accept.lower() == 'y':
        print("Backing up...")
        if os.path.exists(savePathOutput + ".zip"):
            os.remove(savePathOutput + ".zip")
            print("Old backup removed.")
            
        with zipfile.ZipFile(savePathOutput + ".zip", "w", strict_timestamps=False) as zf:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    zf.write(fp, os.path.relpath(fp, path))
        print(f"Backup created at {savePathOutput}.zip")
        
def menuLoop():
    
    print("Choose one of the options below:")
    print(f"1 - Backup Nucleus main folder [{dictPaths["ncPath"][0]}] (Size: {convert_size(get_size(dictPaths["ncPath"][0]))})")
    print(f"2 - Backup Nucleus environment folder [{dictPaths["ncEnvPath"][0]}] (Size: {convert_size(get_size(dictPaths["ncEnvPath"][0]))})")
    print("3 - Exit")
    option = input("Enter your choice: ")
    
    if option == '1' and dictPaths["ncPath"][1]:
        ncMainBackup(dictPaths["ncPath"][0])
    elif option == '2' and dictPaths["ncEnvPath"][1]:
        ncEnvBackup(dictPaths["ncEnvPath"][0])
    elif option == '1' and not dictPaths["ncPath"][1] or option == '2' and not dictPaths["ncEnvPath"][1]:
        print("The folder for this wasnt found!")
        time.sleep(5)
        menuLoop()
    elif option not in ['1', '2', '3']:
        print("Invalid option.")
        time.sleep(5)
        menuLoop()
        
if __name__ == "__main__":        
    try:
        currentUser = os.path.expanduser('~')
        savePathOutput = os.path.join(os.getcwd(),"backup") 
        ncPath = input("Enter your Nucleus Coop installation path: ")

        
        dictPaths = { # bools to check if path exists
            "ncPath": [ncPath, False],
            "ncEnvPath": [os.path.join(currentUser,"NucleusCoop"), False],
        }
        
        if os.path.exists(dictPaths["ncPath"][0]):
            print("Nucleus main folder folder exists!")
            dictPaths["ncPath"][1] = True
        if os.path.exists(dictPaths["ncEnvPath"][0]):
            print("Nucleus Enviromment folder found! (save folder)")
            dictPaths["ncEnvPath"][1] = True
        if not dictPaths["ncPath"][1] and not dictPaths["ncEnvPath"][1]:
            print("Nucleus Enviromment folder and main folder not found!")
            time.sleep(5)
            exit()
            
        menuLoop()
            
    except Exception as e:
        print(f"GENERAL ERROR: {e}")