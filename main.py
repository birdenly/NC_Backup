import os
import time
import tkinter
from tkinter import filedialog

from utils import *


def menuLoop():
    
    sizeMain = convert_size(getSize(dictPaths["ncPath"][0]))
    sizeEnv = convert_size(getSize(dictPaths["ncEnvPath"][0]))
    
    print("\n")
    print("###############################")
    print("Choose one of the options below:")
    print(f"1 - Backup Nucleus main folder [{dictPaths["ncPath"][0]}] (Size: {sizeMain})") if sizeMain != "0B" else print("1 - Backup Nucleus main folder [Not found]")
    print(f"2 - Backup Nucleus environment folder [{dictPaths["ncEnvPath"][0]}] (Size: {sizeEnv})") if sizeEnv != "0B" else print("2 - Backup Nucleus environment folder [Not found]")
    print("3 - Exit")
    option = input("Enter your choice: ")
    
    print("###############################")
    print("\n")
    
    if option == '1' and dictPaths["ncPath"][1]:
        ncMainBackup(dictPaths["ncPath"][0])
        menuLoop()
    elif option == '2' and dictPaths["ncEnvPath"][1]:
        ncEnvBackup(dictPaths["ncEnvPath"][0])
        menuLoop()
    elif option == '1' and not dictPaths["ncPath"][1] or option == '2' and not dictPaths["ncEnvPath"][1]:
        print("The folder for this wasnt found!")
        time.sleep(2)
        menuLoop()
    elif option not in ['1', '2', '3']:
        print("Invalid option.")
        time.sleep(2)
        menuLoop()
        
if __name__ == "__main__":        
    try:
        currentUser = os.path.expanduser('~')
        print("=========== Nucleus Backup ===========")
        print("This tool will help you backup most of your Nucleus Coop save data.\nBut this WONT BACKUP saves for handlers that save in the main game save path(ex: Elden ring, Dark Souls, recent unity game and many others).\nYou will have to backup those manually wherever theythat game saves at.")
        print("\n") 
        print("Please select your Nucleus Coop installation folder on the windowed that opened.")
        tkinter.Tk().withdraw()
        while True:
            ncPath = filedialog.askdirectory(title="Select your Nucleus Coop installation path", mustexist=True)
            if ncPath and os.path.exists(os.path.join(ncPath, "nucleuscoop.exe")):
                break
            print("This is not a valid Nucleus Coop installation folder! try again.")

        
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
        time.sleep(5)