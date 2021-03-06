# SECURE LOGIN DEMO

This is a university project demonstrating a secure user create and login scheme. I've implemented various security measures using a python-based HTTP server. The project implements HTTPs, Content Security Policy (CSP), Password hashing, encryption and various access control methods.<br />
*README en français ci-dessous*

## The languages used are:
1. **Python 3** (tested with version 3.8.8) - the server and back-end processing
2. **HTML** and **JavaScript** - rendering the front-end elements
	
## Tested with
1. **Operating System** - Ubuntu 20.04
2. **Web Browser** - Firefox 92.0 and Chrome 94.0
	
## Instructions - Using a terminal
1. Install python cryptography library
```
pip3 install cryptography
```
2. Install authbind (Otherwise the server must be run as root, not recommended)<br />
```
apt install authbind
```
*NOTE:* Authbind is used to grant onetime access to port 443, for security, this is preferable to running the server as root.<br /><br />
3. Download all files to a common directory
```
git clone https://github.com/GonzoDMX/Secure_Login_Demo.git
```
4. Using a terminal go to the ~/Secure_Login_Demo directory
```
cd ~/Secure_Login_Demo
```
5. Generate a SSL encryption key<br />
```
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
```
*IMPORTANT:* Remember the PEM pass phrase you use to generate the key<br />
It doesn't really matter what you put in the other fields, you can even leave them blank<br /><br />
6. Setup authbind permissions
```
sudo touch /etc/authbind/byport/443
sudo chmod 777 /etc/authbind/byport/443
```
7. Launch the HTTPs Server 'simple_server.py'
```
authbind python3 simple_server.py
```
8. Enter root password when prompted<br />
9. Enter the PEM pass phrase when prompted (that you created in step 4)<br />
10. Using your favorite web browser go to the following url
```
https://localhost
```
*NOTE:* As the SSL certificate is self-signed your web browser may complain about a security risk<br />
Chrome: click *Advanced* -> *Proceed to localhost (unsafe)*<br />
Firefox: click *Advanced...* -> *Accept the Risk and Continue*


## Test Example
You can create new user accounts by clicking the create user button. One account is already registered when first launching the http server.
The preloaded login credentials are:
```
Username: Richard
Password: Password123
```

## IMPORTANT: Notes for Security testing
This demonstration is optimized it for portability. The HTTPs Server does not implement any kind of multithreading so it is highly vulnerable to DOS attacks. Simply connecting from two separate web browsers will cause problems. Additionally, I chose not to implement a proper database for storing user accounts information. Again, the choice was in order to make this program more portable. Since you will be running the server locally it would be relatively easy to reverse engineer the security by reading the source code. For testing purposes lets assume that your only access point is the web browser / network, as would be the case if this were a deployed website.

Lastly, and maybe it doesn't need to be said, this program is not fit for production. It might be a suitable example for lightweight hobby projects running on a local network. However, consider yourself warned, if you use this code to deploy a website you're gonna have a bad time.


---


# SECURE LOGIN DEMO_FR

Il s'agit d'un projet universitaire démontrant un schéma sécurisé de création et de connexion d'utilisateurs. J'ai mis en place diverses mesures de sécurité à l'aide d'un serveur HTTP basé sur Python. Le projet implémente les HTTPs, la Content Security Policy (CSP), le hachage de mot de passe, le cryptage et diverses méthodes de contrôle d'accès.

## Les langages de programmation utilisés sont:
1. **Python 3** (version 3.8.8) - utilisé pour le serveur et le traitement back-end
2. **HTML** et **JavaScript** - utilisé pour rendre les éléments front-end
	
## Testé avec
1. **Système d'exploitation** - Ubuntu 20.04
2. **Navigateur Web** - Firefox 92.0 et Chrome 94.0
	
## Instructions - Utilisation de la ligne de commande
1. Installer la librarie de cryptographie python
```
pip3 install cryptography
```
2. Installer authbind (Sinon, le serveur doit être exécuté en tant que root, non recommandé)<br />
```
apt install authbind
```
*NOTE:* Authbind est utilisé pour accorder un accès au port 443.<br /><br />
3. Télécharger tous les fichiers dans un répertoire commun
```
git clone https://github.com/GonzoDMX/Secure_Login_Demo.git
```
4. A l'aide d'un terminal allez dans le répertoire ~/Secure_Login_Demo
```
cd ~/Secure_Login_Demo
```
5. Générer une clé de cryptage SSL<br />
```
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
```
*IMPORTANT:* Ne pas oublier pas le mot de passe PEM que vous utilisez pour générer la clé<br />
Les autres champs n'ont pas d'importance, vous pouvez même les laisser vides<br /><br />
6. Configurer les autorisations du authbind
```
sudo touch /etc/authbind/byport/443
sudo chmod 777 /etc/authbind/byport/443
```
7. Lancer le serveur HTTPs 'simple_server.py'
```
authbind python3 simple_server.py
```
8. Entrer le mot de passe root lorsque vous y êtes invité<br />
9. Entrer le mot de passe PEM lorsque vous y êtes invité (créé à l'étape 4)<br />
10. À l'aide de votre navigateur Web préféré, accédez à l'URL suivante
```
https://localhost:8000
```
*NOTE:* Le certificat SSL étant auto-signé, votre navigateur Web peut se plaindre d'un risque de sécurité<br />
Chrome: cliquer *Advanced* puis *Proceed to localhost (unsafe)*<br />
Firefox: cliquer *Advanced...* puis *Accept the Risk and Continue*


## L'exemple de test
Vous pouvez créer de nouveaux comptes d'utilisateurs en cliquant sur le bouton 'Create User'. Un compte est déjà enregistré lors du premier lancement du serveur http.
Les identifiants de connexion préchargés sont:
```
Nom d'utilisateur: Richard
Le mot de passe:   Password123
```

## Remarque pour les tests de sécurité
Cette démonstration est optimisée pour la portabilité. Le serveur HTTPs n'implémente aucun type de multithreading, il est donc très vulnérable aux attaques DOS. Le simple fait de se connecter à partir de deux navigateurs Web en même temps distincts causera des problèmes. De plus, j'ai choisi de ne pas implémenter une base de données pour stocker les informations des comptes d'utilisateurs. Encore une fois, le choix était de rendre ce programme plus portable. Étant donné que vous exécuterez le serveur localement, il serait relativement facile de déconstruire la sécurité en lisant le code source. À des fins de test, supposons que votre seul point d'accès est le navigateur Web / réseau  (Comme s'il s'agissait d'un site Web déployé).

Enfin, et peut-être qu'il n'est pas nécessaire de le dire, ce programme n'est pas adapté à la production. Cela peut être un exemple approprié pour les projets de loisirs exécutés sur un réseau local. Cependant, considérez-vous prévenu, si vous utilisez ce code pour déployer un site Web, vous allez avoir du mal.
