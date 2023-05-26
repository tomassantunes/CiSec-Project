import os
import base64
import sys
import StringIO
from Crypto import Random
from Crypto.Cipher import AES

def encrypt(data, filename):
	source = open(filename + "-copy", "r")

	iv = Random.new().read(AES.block_size)
	cipher = AES.new(StringIO.StringIO(source).read(24), AES.MODE_CFB, iv)
	encrypted = iv + cipher.encrypt(data)

	source.close()
	return base64.b64encode(encrypted)

