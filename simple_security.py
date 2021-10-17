#!/usr/bin/env python3

"""
	Crypto functions for supporting the Python HTTP Server
	Créé par: Andrew O'Shei
"""

import ast
import string
import random
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet

key_path = ".password.pass"

# Returns a hash of the input string
def hash_it(key):
	h = hashlib.new('sha3_512')
	h.update(key.encode('utf-8'))
	return h.hexdigest()
	
# Generates a random key
def keygen():
	return Fernet.generate_key()
	
# Encrypt input data string with provided key
def encrypt(data):
	key = get_key()
	try:
		k = Fernet(key)
		return k.encrypt(data.encode('utf-8'))
	except Exception as e:
		print(e)
	
# Decrypt data with provided key
def decrypt(data):
	key = get_key()
	try:
		k = Fernet(key)
		return k.decrypt(data).decode('utf-8')
	except Exception as e:
		print(e)
	
# Get the key
def get_key():
	global key_path
	if Path(key_path).is_file():
		f = open(key_path, "rb")
		key = f.read()
		f.close()
		return key
	else:
		return None
		
		
# Check that key exists otherwise generate a key
def key_check():
	global key_path
	if not Path(key_path).is_file():
		try:
			f = open(key_path, "wb+")
			f.write(keygen())
			f.close()
		except Exception as e:
			print(e)

# Generates a random string, used for validating a session
def random_string(length):
	letters = string.ascii_letters + string.digits
	result_str = ''.join(random.choice(letters) for i in range(length))
	return result_str

# Check that the username is valid
def name_check(user):
	allowed = set(string.ascii_letters + string.digits + '_')
	if set(user) <= allowed:
		return True
	return False
	
# Check that password is valid
def pwd_check(pwd1, pwd2):
	if pwd1 == pwd2 and len(pwd1) > 8 and pwd1.isprintable():
		return True
	return False

# Converts a string to dictionary
def convert_dict(data):
	return ast.literal_eval(data)

