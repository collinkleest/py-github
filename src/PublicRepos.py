#-- import --#
import requests as req
from time import sleep


class PublicRepos:

    def __init__(self):
        self.ROOT_API = "https://api.github.com"
        self.promptForUser()

    def promptForUser(self):
        user = str(input("User: "))
        self.getUserRepos(user)

    def getUserRepos(self, user):
        r = req.get(self.ROOT_API + "/users/" + user + "/repos")
        data = r.json()
        for i in data:
            print(i['name'] + " | " + i['svn_url'])
        sleep(.7)
