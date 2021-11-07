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

import ssl
import urllib.parse as up
from pathlib import Path
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

import simple_security as ss


session_string = ""

restricted_words = [".pass", ".db", ".py"]

valid_pages = list()

users_path = ".my_accounts.db"

""" CSP Headers to defend agains XSS attacks"""
login_header = "default-src 'self'; child-src 'none'; object-src 'none'; script-src 'sha256-4BSlqwTfCxFbiFBfWZBcDxmjyvXL2ynJUFqLRCwGFxY='; img-src 'self'; style-src 'sha256-TLI54zo4PpnrkdpCMKoxPCugLTUKPc9+4l3zHD3jY5k='"

create_header = "default-src 'self'; child-src 'none'; object-src 'none'; script-src 'self' 'sha256-QOBtvJcHLER/MHDRFA8eJII/SsvBwaFyuzOqI4GNBiM='; img-src 'self'; style-src 'sha256-TLI54zo4PpnrkdpCMKoxPCugLTUKPc9+4l3zHD3jY5k='"

message_header = "default-src 'self'; child-src 'none'; object-src 'none'; script-src 'sha256-fZhG2bh1opVQ+neDYdEzZcNPV/SbhhdP8l+/+xGBdn4='; img-src 'self'; style-src 'sha256-TLI54zo4PpnrkdpCMKoxPCugLTUKPc9+4l3zHD3jY5k='"

welcome_header = "default-src 'self'; child-src 'none'; object-src 'none'; script-src 'sha256-fZhG2bh1opVQ+neDYdEzZcNPV/SbhhdP8l+/+xGBdn4='; img-src 'self'; style-src 'sha256-8nKI3BVBQRYZ/xsA+lWQzWffMS1/2WoV4jzan5Ekct0='"

error_header = "default-src 'self'; child-src 'none'; object-src 'none'; script-src 'sha256-fZhG2bh1opVQ+neDYdEzZcNPV/SbhhdP8l+/+xGBdn4='; img-src 'self'; style-src 'sha256-TLI54zo4PpnrkdpCMKoxPCugLTUKPc9+4l3zHD3jY5k='"

collision_header = "default-src 'self'; child-src 'none'; object-src 'none'; script-src 'sha256-eP0G2JixgtEZmzxjdbJjtBslaaWwZYGF9OsTEVmz3Wc='; img-src 'self'; style-src 'sha256-TLI54zo4PpnrkdpCMKoxPCugLTUKPc9+4l3zHD3jY5k='"


""" Simple HTTP Server that handles GET and POST """
class WebServer(BaseHTTPRequestHandler):

	# Set HTML Doc type headers
	def _set_headers(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		if "login_page.html" in self.path:
			self.send_header("Content-Security-Policy", login_header)
		elif "create_page.html" in self.path:
			self.send_header("Content-Security-Policy", create_header)
		elif "welcome_page.html" in self.path:
			self.send_header("Content-Security-Policy", welcome_header)
		elif "name_collision.html" in self.path:
			self.send_header("Content-Security-Policy", collision_header)
		elif "error_page.html" in self.path or "access_refused.html" in self.path:
			self.send_header("Content-Security-Policy", error_header)
		else:
			self.send_header("Content-Security-Policy", message_header)
		self.end_headers()

	# Push GET Request to Clients
	def do_GET(self):
		global session_string
		global restricted_words
		# Check path, if none send to home page
		if self.path == '/':
			self.path = "/index.html"
		# Check for illegal access
		for elem in restricted_words:
			if elem in self.path:
				self.path = "/access_refused.html"
		if self.path[1:] not in valid_pages:
			self.path = "/error_404.html"
		self.do_KICK(self.path)


	def do_HEAD(self):
		self._set_headers()
	
	# Retrieve POST Data
	def do_POST(self):
		global session_string
		content_len = int(self.headers['Content-Length'])
		# Get POST data as decoded byte string
		post_data = self.rfile.read(content_len).decode('utf-8')
		# Convert POST data to dictionary of lists
		parsed_data = up.parse_qs(post_data)
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
					print("Log: User " + user + " has logged in successfully!")
			elif form_type == "create":
				user = parsed_data['user'][0]
				pwd1 = parsed_data['pwd1'][0]
				pwd2 = parsed_data['pwd2'][0]
				secret = parsed_data['secret'][0]
				if self.user_create(user, pwd1, pwd2, secret):
					print("Log: New user " + user + " created successfully!")
					

	# Feed Client the target page
	def do_KICK(self, target):
		global session_string
		self.path = target
		self._set_headers()
		# for handling images
		if target[-4:] == ".jpg" or target[-4:] == ".ico":
			html = open(target[1:], "rb").read()
			# Push image to client
			self.wfile.write(html)
		elif target[-4:] == "html":
			# Read HTML doc as String
			html = open(target[1:], "r").read()
			# If accessing login or create page set Session Id
			if target == "/login_page.html" or target == "/create_page.html":
				# Generate session ID string and overwrite session Id value in HTML
				session_string = ss.random_string(16)
				# Overwrite default session id
				html = html.replace("12345", session_string)
			# Push web page to client
			self.wfile.write(html.encode('utf-8'))
		
	# Method for logging into user account
	def user_login(self, user, pwd):
		# Check if Javascript has been disactivated
		if not ss.name_check(user) or not ss.pwd_check(pwd, pwd):
			self.do_KICK("/error_page.html")
			return False
		data = self.get_data()
		# Check if user is in database
		if user in data:
			h = ss.hash_it(pwd)
			if h == data[user]["Key"]:
				secret = data[user]["Secret"]
				data.clear()
				self.do_LOGIN(user, secret)
				return True
			# Password is not correct!
			else:
				data.clear()
				self.do_KICK("/access_refused.html")
				return False
		# User does not exist in database
		else:
			data.clear()
			self.do_KICK("/access_refused.html")
			return False
		
	def user_create(self, user, pwd1, pwd2, secret):
		# Check if Javascript has been disactivated
		if not ss.name_check(user) or not ss.pwd_check(pwd1, pwd2):
			self.do_KICK("/error_page.html")
			return False
		data = self.get_data()
		# Check if Username already exists
		if user in data:
			self.do_KICK("/name_collision.html")
			return False
		else:
			key = ss.hash_it(pwd1)
			data[user] = {"Secret":secret, "Key":key}
			if self.write_data(data):
				data.clear()
				self.do_KICK("/new_user.html")
				return True
			# If file failed to write
			else:
				data.clear()
				self.do_KICK("/error_page.html")
				return False

	# Send user to Welcome page
	def do_LOGIN(self, user, secret):
		self.path = "/welcome_page.html"
		self._set_headers()
		html = open(self.path[1:], "r").read()
		html = html.replace("USERNAME", user).replace("MESSAGE", secret)
		self.wfile.write(html.encode('utf-8'))
		

	# Get decrypted data as a dict
	def get_data(self):
		global users_path
		f = open(users_path, "rb")
		data = ss.convert_dict(ss.decrypt(f.read()))
		f.close()
		return data
		
	# Encrypt data and write to file
	def write_data(self, data):
		global users_path
		try:
			f = open(users_path, "wb+")
			f.write(ss.encrypt(str(data)))
			f.close()
			return True
		except Exception as e:
			print(e)
			return False

def run(server_class=HTTPServer, handler_class=WebServer, addr="localhost", port=8000):
	server_address = (addr, port)
	httpd = server_class(server_address, handler_class)
	try:
		httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, keyfile="key.pem", certfile="cert.pem", ssl_version=ssl.PROTOCOL_TLS)
		print(f"Starting http server on {addr}:{port}")
		try:
			httpd.serve_forever()
		except KeyboardInterrupt:
			pass
		httpd.server_close()
	except FileNotFoundError:
		print("ERROR: Cannot start server, unable to find SSL Certificates")
		print("Hint: Please review README.md for instructions")


# Set Database with demo entry,
def on_first_entry():
	global users_path
	if not Path(users_path).is_file():
		quote = "With software there are only two possibilities: either the users control the program or the program controls the users. -RMS"
		pwd = "Password123"
		key = ss.hash_it(pwd)
		demo_entry = {"Richard":{"Secret":quote, "Key":key}}
		try:
			f = open(users_path, "wb+")
			f.write(ss.encrypt(str(demo_entry)))
			os.chmod(users_path, 0o665)
			f.close()
		except Exception as e:
			print(e)
	else:
		pass

# Decrypt and return data as dict example
def test_entry():
	global users_path
	if Path(users_path).is_file():
		try:
			f = open(users_path, "rb")
			d = ss.decrypt(f.read())
			print(d)					# Print Data as string
			data = ss.convert_dict(d)
			print(str(data))			# Print Data as dictionary
			f.close()
		except Exception as e:
			print(e)

def get_valid():
	global valid_pages
	for file in os.listdir(os.getcwd()):
		if file.endswith(".html"):
			if file != "welcome_page.html":
				valid_pages.append(file)
		if file.endswith(".css"):
			valid_pages.append(file)
	for file in os.listdir(os.getcwd() + "/assets"):
		if file.endswith(".jpg"):
			valid_pages.append("assets/" + file)
	print(valid_pages)

if __name__ == "__main__":
	ss.key_check()
	on_first_entry()
	get_valid()
	# test_entry()
	run(addr="localhost", port=443)
    
    
