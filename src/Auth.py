#-- imports --#
import requests as req
import json
import os
from logzero import logging


class Auth:

    def __init__(self):
        self.ROOT_API = "https://api.github.com"
        self.userName = ''
        self.token = ''
        self.SAVE_CREDENTIALS = False
        self.authenticated = False
        self.authenticate()

    def activeCredenitalsPresent(self):
        if(os.path.exists("data/secrets.json")):
            with open('data/secrets.json') as file:
                data = json.load(file)
                self.SAVE_CREDENTIALS = True
                if(self.checkAuth(data['userName'], data['token'])):
                    return True
                else:
                    return False

    def checkAuth(self, uName, token):
        r = req.get(self.ROOT_API + '/user', auth=(uName, token))
        if (r.status_code == 200):
            logging.info("Authentication success for:", r.json()['login'])
            self.userName = uName
            self.token = token
            return True
        else:
            return False

    def authenticate(self):
        if(self.activeCredenitalsPresent()):
            self.authenticated = True
            return {'userName': self.userName, 'token': self.token}

        while not self.authenticated:
            userName = str(input("Username: ")).strip()
            token = str(input("Token: ")).strip()
            r = req.get(self.ROOT_API + '/user', auth=(userName, token))
            if (r.status_code == 200):
                logging.info("Authentication success for:", r.json()['login'])
                self.authenticated = True
                credentials = {
                    "userName": userName,
                    "token": token
                }
                self.userName = userName
                self.token = token
                with open('data/secrets.json', 'w') as outfile:
                    json.dump(credentials, outfile)
                save = str(
                    input("Would you like your credentials saved for later (y/n): "))
                save = save.lower().strip()
                if (save == 'y' or save == 'yes'):
                    print('saving your credentials')
                    self.SAVE_CREDENTIALS = True
                else:
                    print("Credentials will be deleted after session")
                return {'userName': self.userName, 'token': self.token}
            else:
                logging.error('Failed to autheticate')
                statusCode = "Status: " + str(r.status_code)
                logging.error(statusCode)
                logging.error("Server Response:" + str(r.json()))
