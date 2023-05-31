import os
import base64
import sys
from cryptography.fernet import Fernet

KEY = b'k6XGrVRO4bCexC54uWlJgKPx9KloztECXpA-LywXDKo='

if __name__ == "__main__":
	to_decrypt = "processhacker-2.39-setup.exeHAHAHA"
	with open(to_decrypt, "rb") as file:
		data = file.read()

	f = Fernet(KEY)
	decrypted = f.decrypt(data)
	
	with open("test.exe", "wb") as file_exe:
		file.write(decrypted)