#-- imports --#
import requests as req
import json
import os
import sys

#-- class imports --#
from Auth import Auth
from Options import Options


class App:

    def __init__(self):
        self.authObject = Auth()
        self.credentials = self.authObject.authenticate()

    def deleteCredentials(self):
        if not (self.authObject.SAVE_CREDENTIALS):
            if (os.path.exists('data/secrets.json')):
                os.remove('data/secrets.json')


if __name__ == "__main__":
    app = App()
    app.deleteCredentials()
    while True:
        try:
            optionsObject = Options(
                app.credentials['userName'], app.credentials['token'])
        except KeyboardInterrupt:
            print("bye")
            sys.exit()
