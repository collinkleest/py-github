#-- imports --#
import json
import requests as req
from PyInquirer import prompt, print_json
from logzero import logger
from time import sleep


class Repositories:

    def __init__(self, choice, uName, uToken):
        self.ROOT_API = "https://api.github.com"
        self.userName = uName
        self.token = uToken
        self.repoChoice = ""
        if (choice == 'change'):
            self.getRepos()
        elif (choice == 'create'):
            self.createRepository()

    def getRepos(self):
        self.getCredentials()
        r = req.get('https://api.github.com/user/repos',
                    auth=(self.userName, self.token))
        repoChoices = []
        for i in r.json():
            repoChoices.append(i['name'])

        rChoice = prompt([{'type': 'list', 'name': 'repo-options',
                           'message': 'Choose a repo', 'choices': repoChoices}])

        self.repoChoice = rChoice['repo-options']

        todoChoice = prompt([{'type': 'list', 'name': 'repo-options',
                              'message': 'Choose a repo',
                              'choices': ['Change the repo', 'Delete a repo', 'Create a repo']}])

        if (todoChoice['repo-options'] == 'Change the repo'):
            self.changeRepo(self.repoChoice)
        elif (todoChoice['repo-options'] == 'Delete a repo'):
            self.deleteRepo(self.repoChoice)

    def changeRepo(self, repoName):
        name = str(input("Repo Name (leave blank to not change): "))
        desc = str(input("Description (leave blank to not change): "))
        homePage = str(input("Home Page Url (leave blank to not change): "))
        questions = [
            {'type': 'confirm', 'name': 'private', 'message': 'Private?'},
            {'type': 'confirm', 'name': 'issues', 'message': 'Has Issues?'},
            {'type': 'confirm', 'name': 'projects', 'message': 'Projects?'},
            {'type': 'confirm', 'name': 'wiki', 'message': 'Wiki?'},
        ]
        answers = prompt(questions)
        data = {
            "name": name,
            "description": desc,
            "homepage": homePage,
            "private": answers['private'],
            "has_issues": answers['issues'],
            "has_projects": answers['projects'],
            "has_wiki": answers['wiki']
        }
        r = req.patch(self.ROOT_API + "/repos/" + self.userName + "/" +
                      repoName, auth=(self.userName, self.token), data=json.dumps(data))
        if (r.status_code == 200):
            print("Successfully modified repo:", repoName)
            sleep(.7)
        else:
            print("Repo wasnt successfully modified")
            sleep(.7)

    def deleteRepo(self, repoName):
        shouldDelete = prompt(
            {'type': 'confirm', 'name': 'delete', 'message': 'You sure you want to delete?'})
        if (shouldDelete['delete']):
            r = req.delete(self.ROOT_API + "/repos/" +
                           self.userName + "/" + repoName)
            if (r.status_code == 204):
                print(repoName, "deleted")
            elif (r.status_code == 403):
                print(r.json())
                print("You are not the owner of this repo")

    def getCredentials(self):
        with open('data/secrets.json') as file:
            data = json.load(file)
            self.userName = data['userName']
            self.token = data['token']

    def getLicenses(self):
        licenseJson = req.get(self.ROOT_API + '/licenses')
        licenseJson = licenseJson.json()
        licenses = []
        for i in licenseJson:
            licenses.append(i['key'])
        return licenses

    def createRepository(self):
        name = str(input("Repo Name (leave blank to not change): ")).strip()
        desc = str(input("Description (leave blank to not change): ")).strip()
        homePage = str(
            input("Home Page Url (leave blank to not change): ")).strip()
        logger.info('Retrieving .gitignore templates')
        gitIgnoreTemplates = req.get(
            self.ROOT_API + '/gitignore/templates').json()
        logger.info('Retrieving Licenses')
        licenses = self.getLicenses()
        questions = [
            {'type': 'confirm', 'name': 'private', 'message': 'Private?'},
            {'type': 'confirm', 'name': 'issues', 'message': 'Has Issues?'},
            {'type': 'confirm', 'name': 'projects', 'message': 'Projects?'},
            {'type': 'confirm', 'name': 'wiki', 'message': 'Wiki?'},
            {'type': 'confirm', 'name': 'readme', 'message': 'README.md?'},
            {'type': 'list', 'name': 'git_templates',
                'message': 'Choose a gitignore template', 'choices': gitIgnoreTemplates},
            {'type': 'list', 'name': 'licenses',
             'message': 'Choose a gitignore template', 'choices': licenses}
        ]
        answers = prompt(questions)
        data = {
            "name": name,
            "description": desc,
            "homepage": homePage,
            "private": answers['private'],
            "has_issues": answers['issues'],
            "has_projects": answers['projects'],
            "has_wiki": answers['wiki'],
            "auto_init": answers['readme'],
            "gitignore_template	": answers['git_templates'],
            "license_template": answers['licenses']
        }
        r = req.post(self.ROOT_API + '/user/repos',
                     auth=(self.userName, self.token), data=json.dumps(data))
        if (r.status_code == 201):
            logger.info("Repo Created!")
            sleep(.7)
        else:
            logger.error("Repo failed to create")
            sleep(.7)
