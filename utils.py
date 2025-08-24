import math
import os
import shutil
import zipfile

OUTPUTMAIN = os.path.join(os.getcwd(),"backup_main.zip")
OUTPUTENV = os.path.join(os.getcwd(),"backup_env.zip")

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def getSize(path):
    # Return total size of files to be backed up.
    try:
        entries = os.listdir(path)
    except OSError:
        return 0

    has_nc_exe = any(name.lower() == "nucleuscoop.exe" for name in entries)

    total_size = 0
    if not has_nc_exe:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                filePath = os.path.join(dirpath, f)
                try:
                    total_size += os.path.getsize(filePath)
                except OSError:
                    pass
        return total_size
    
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            filePath = os.path.join(dirpath, file)
            try:
                if file == "Settings.ini":
                    total_size += os.path.getsize(filePath)
                    continue
                if os.path.basename(dirpath) in ["game profiles", "Profiles"]:
                    root, ext = os.path.splitext(filePath)
                    if os.path.islink(filePath):
                        continue
                    if ext.lower() in [".exe", ".log"]:
                        continue
                    if file.lower().startswith("steam_api") and ext.lower() == ".dll":
                        continue
                    total_size += os.path.getsize(filePath)
                    
                #logic to get the content folder and the subdirs
                sub = os.path.join(dirpath, file)
                parent = os.path.join(path, "content")
                if sub.startswith(parent):
                    root, extension = os.path.splitext(os.path.join(dirpath, file))
                    if os.path.islink(os.path.join(dirpath, file)):
                        continue
                    if extension in [".exe", ".log"]:
                        continue
                    total_size += os.path.getsize(filePath)
            except OSError:
                pass
    return total_size

def backupExist(output):
    if os.path.exists(output):
        print("\n")
        print("Backup already exists, do you want to remove it? (y/n)")
        inputChoice = input().lower()
        if inputChoice == 'y':
            os.remove(output)
            print("Old backup removed.")
            return False
        else:
            shutil.move(output, output + ".bak")
            print(f"Old backup has been changed to {output}.bak")
            return True
    else:
        return False
        
        

def ncEnvBackup(path):
    print("Backing up environment folder...")
    backupExist(OUTPUTENV)
    
    with zipfile.ZipFile(OUTPUTENV, "w", strict_timestamps=False) as zf:
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                final = os.path.join(dirpath, file)
                finalPath = os.path.join("NucleusCoop", os.path.relpath(final, path))
                zf.write(final, finalPath)
                print("File done: " + finalPath)
    print(f"Backup created at {OUTPUTENV}")

        
def ncMainBackup(path):
    print("Backing up main folder...")
    backupExist(OUTPUTMAIN)
    with zipfile.ZipFile(OUTPUTMAIN, "w", strict_timestamps=False) as zf:
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                #always get settings.ini
                if file == "Settings.ini": 
                    final = os.path.join(dirpath, file)
                    zf.write(final, os.path.relpath(final, path))
                
                #only get the main ones
                if os.path.basename(dirpath) in ["game profiles", "Profiles"]:
                    root, extension = os.path.splitext(os.path.join(dirpath, file))
                    if os.path.islink(os.path.join(dirpath, file)):
                        continue
                    if extension.lower() in [".exe", ".log"]:
                        continue
                    if file.lower().startswith("steam_api") and extension.lower() == ".dll":
                        continue
                    final = os.path.join(dirpath, file)
                    zf.write(final, os.path.relpath(final, path))
                    print("File done: " + final)           
                         
                #logic to get the content folder and the subdirs
                sub = os.path.join(dirpath, file)
                parent = os.path.join(path, "content")
                if sub.startswith(parent):
                    root, extension = os.path.splitext(os.path.join(dirpath, file))
                    if os.path.islink(os.path.join(dirpath, file)):
                        continue
                    if extension in [".exe", ".log"]:
                        continue
                    final = os.path.join(dirpath, file)
                    zf.write(final, os.path.relpath(final, path))
                    print("File done: " + final)
                
    print(f"Backup created at {OUTPUTMAIN}")