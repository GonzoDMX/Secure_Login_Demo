# SECURE LOGIN DEMO

This is a university project demonstrating a secure user create and login scheme. 

## The languages used are:
1. **Python** (tested with version 3.8.8) - for the server and back-end processing
2. **html** and **javascript** - for rendering the front end user facing elements.
	
## Tested with
1. **Operating System** - Ubuntu 20.04
2. **Brower** - Firefox 92.0 and Chrome 94.0
	
## Instructions
1. Install python cryptography library
```
pip3 install cryptography
```
2. Download all files to a common repository
```
git clone https://github.com/GonzoDMX/Secure_Login_Demo.git
```
3. Using a terminal go to the Secure_Login_Demo directory and launch the simple_server.py HTTP server
```
cd ~/Secure_Login_Demo
python3 simple_server.py
```
4. Using your favorite web browser go to the following url
```
http://localhost:8000
```
5. Try to break the app

## Test Example
You can create new user accounts by clicking the create user button. One account is already registered when first launching the http server. To test the login credentials are:
```
Username: Richard
Password: Password123
```

## Note for Security testing
This demonstration is a bit contrived. Since you will be running the server locally it would be relatively easy to reverse engineer the security by reading the source code. For testing purposes lets assume that your only access point is the web browser / network, as would be the case if this were a deployed website.
