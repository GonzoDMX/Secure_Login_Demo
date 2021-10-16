#!/usr/bin/env python3

"""
	Python-Based HTTTP Server 
	Créé par: Andrew O'Shei
	
	Il s'agit d'un simple serveur http pour une application
	de création et de connexion d'utilisateurs.
	Un serveur Web basé sur Python a été choisi pour rendre
	le projet plus portable, il peut donc être exécuté sans
	installer quelque chose comme un serveur Apache.
	
	Instructions:
	1. Lancez le serveur Web à partir de la ligne de commande avec python3
	2. Ouvrez un navigateur Web et accédez à l'URL: http://localhost:8000
	   (Testé sur Ubuntu 20.04 avec Python 3.8.8 et Firefox 92.0)
"""

import random
import string
import urllib.parse as up
from pathlib import Path
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

from cryptography.fernet import Fernet


session_string = ""

""" Simple HTTP Server that handles GET and POST """
class WebServer(BaseHTTPRequestHandler):
	# Generates a random string, used for validating a session
	def random_string(self, length):
		letters = string.ascii_lowercase
		result_str = ''.join(random.choice(letters) for i in range(length))
		return result_str

	# Set HTML Doc type headers
	def _set_headers(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	# Push GET Request to Clients
	def do_GET(self):
		global session_string
		# Check path, if none send to home page
		if self.path == '/':
			# self.path = "/access_refused.html"
			self.path = "/index.html"
		self._set_headers()
		# for handling images
		if self.path[-4:] == ".jpg" or self.path[-4:] == ".ico":
			html = open(self.path[1:], "rb").read()
			# Push image to client
			self.wfile.write(html)
		elif self.path[-4:] == "html":
			# Read HTML doc as String
			html = open(self.path[1:], "r").read()
			# Generate session ID string and overwrite session Id value in HTML
			session_string = self.random_string(10)
			if self.path == "/login_page.html" or self.path == "/create_page.html":
				html = html.replace("12345", session_string)
			# Push web page to client
			self.wfile.write(html.encode('utf-8'))

	def do_HEAD(self):
		self._set_headers()
	
	# Retrieve POST Data
	def do_POST(self):
		global session_string
		content_len = int(self.headers['Content-Length'])
		# Get POST data as decoded byte string
		post_data = self.rfile.read(content_len).decode('utf-8')
		self._set_headers()
		# Convert POST data to dictionary of lists
		parsed_data = up.parse_qs(post_data)
		print("This is Parsed data: " + str(parsed_data))
		form_type = parsed_data['formId'][0]
		session_id = parsed_data['sessionId'][0]
		if session_id != session_string:
			# INVALID Session ID, send Client to Timeout Screen
			self.do_KICK("/session_timeout.html")
		elif session_id == session_string:
			# Session ID is VALID
			if form_type == "login":
				user = parsed_data['user'][0]
				pwd = parsed_data['pwd'][0]
				if self.user_login(user, pwd):
					print("Success!")
				else:
					self.do_KICK("/access_refused.html")
			elif form_type == "create":
				user = parsed_data['user'][0]
				pwd = parsed_data['pwd1'][0]
				secret = parsed_data['secret'][0]
				print(secret)
				if self.user_create(user, pwd):
					# TODO: Create Success Screen
					print("Success!")
				else:
					self.do_KICK("/name_collision.html")
				

	# Kick Client to target path
	def do_KICK(self, target):
		self.path = target
		self._set_headers
		html = open(self.path[1:], "r").read()
		self.wfile.write(html.encode('utf-8'))
		
	def user_login(self, user, pwd):
		# TODO: Check user name and password here
		return False
		
	def user_create(self, user, pwd):
		# TODO: Check for users with same name, register new user
		return False
		
		
	def encrypt(self, data):
		k = Fernet(self.get_key())
		return k.encrypt(data.encode())
		
	def decrypt(self, data):
		k = Fernet(self.get_key())
		return k.decrypt(data)
		
	def get_key(self):
		dir_path = os.cwd()
		f_path = dir_path + "/.password.pass"
		return open(f_path, "rb").read()


def run(server_class=HTTPServer, handler_class=WebServer, addr="localhost", port=8000):
	server_address = (addr, port)
	httpd = server_class(server_address, handler_class)

	print(f"Starting httpd server on {addr}:{port}")
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()

def on_first():
	dir_path = os.getcwd()
	f_path = dir_path + "/.password.pass"
	if not Path(f_path).is_file():
		try:
			p_file = open(".password.pass", "wb+")
			key = Fernet.generate_key()
			p_file.write(key)
			p_file.close()
		except Exception as e:
			print(e)
	else:
		pass

if __name__ == "__main__":
	on_first()
	run(addr="localhost", port=8000)
    
    
