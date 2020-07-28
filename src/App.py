# imports
import requests as req
import json
import os

# global variables
ROOT_API = "https://api.github.com"
SAVE_CREDENTIALS = False


def activeCredenitalsPresent():
    if(os.path.exists("data/secrets.json")):
        with open('data/secrets.json') as file:
            data = json.load(file)
            if(checkAuth(data['userName'], data['token'])):
                return True
            else:
                return False


def checkAuth(uName, token):
    r = req.get(ROOT_API + '/user', auth=(uName, token))
    if (r.status_code == 200):
        return True
    else:
        return False


def authenticate():
    authenticated = False

    if(activeCredenitalsPresent()):
        authenticated = True

    while not authenticated:
        userName = str(input("Username: ")).strip()
        token = str(input("Token: ")).strip()
        r = req.get(ROOT_API + '/user', auth=(userName, token))
        if (r.status_code == 200):
            authenticated = True
            credentials = {
                "userName": userName,
                "token": token
            }
            with open('data/secrets.json', 'w') as outfile:
                json.dump(credentials, outfile)
            save = str(
                input("Would you like your credentials saved for later (y/n):"))
            save = save.lower().strip()
            if (save == 'y' or save == 'yes'):
                print('saving your credentials')
            else:
                print("Credentials will be delted after session")
        else:
            print('failed to autheticate')
            print("status:", r.status_code)
            print("response:", r.json())


authenticate()
