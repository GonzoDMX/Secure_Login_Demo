# SECURE LOGIN DEMO

This is a university project demonstrating a secure user create and login scheme. 
*README en français ci-dessous*

## The languages used are:
1. **Python 3** (tested with version 3.8.8) - the server and back-end processing
2. **HTML** and **JavaScript** - rendering the front-end elements
	
## Tested with
1. **Operating System** - Ubuntu 20.04
2. **Web Browser** - Firefox 92.0 and Chrome 94.0
	
## Instructions
1. Install python cryptography library
```
pip3 install cryptography
```
2. Download all files to a common directory
```
git clone https://github.com/GonzoDMX/Secure_Login_Demo.git
```
3. Using a terminal go to the ~/Secure_Login_Demo directory and launch the HTTP Server 'simple_server.py'
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
You can create new user accounts by clicking the create user button. One account is already registered when first launching the http server.
The preloaded login credentials are:
```
Username: Richard
Password: Password123
```

## Note for Security testing
This demonstration is a bit contrived. Since you will be running the server locally it would be relatively easy to reverse engineer the security by reading the source code. For testing purposes lets assume that your only access point is the web browser / network, as would be the case if this were a deployed website.




# SECURE LOGIN DEMO_FR

Il s'agit d'un projet universitaire démontrant un schéma sécurisé de création et de connexion d'utilisateurs. 

## Les langages de programmation utilisés sont:
1. **Python 3** (version 3.8.8) - utilisé pour le serveur et le traitement back-end
2. **HTML** et **JavaScript** - utilisé pour rendre les éléments front-end
	
## Testé avec
1. **Système d'exploitation** - Ubuntu 20.04
2. **Navigateur Web** - Firefox 92.0 et Chrome 94.0
	
## Instructions
1. Installer la librarie de cryptographie python
```
pip3 install cryptography
```
2. Télécharger tous les fichiers dans un répertoire commun
```
git clone https://github.com/GonzoDMX/Secure_Login_Demo.git
```
3. A l'aide d'un terminal allez dans le répertoire ~/Secure_Login_Demo et lancez le serveur HTTP 'simple_server.py'
```
cd ~/Secure_Login_Demo
python3 simple_server.py
```
4. À l'aide de votre navigateur Web préféré, accédez à l'URL suivante
```
http://localhost:8000
```
5. Essayez de casser l'application

## L'exemple de test
Vous pouvez créer de nouveaux comptes d'utilisateurs en cliquant sur le bouton 'Create User'. Un compte est déjà enregistré lors du premier lancement du serveur http.
Les identifiants de connexion préchargés sont:
```
Nom d'utilisateur: Richard
Le mot de passe:   Password123
```

## Remarque pour les tests de sécurité
Cette démonstration est un peu artificielle. Étant donné que vous exécuterez le serveur localement, il serait relativement facile de désosser la sécurité en lisant le code source. À des fins de test, supposons que votre seul point d'accès est le navigateur Web / réseau (Comme s'il s'agissait d'un site Web déployé).
