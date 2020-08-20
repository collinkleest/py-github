#-- imports --#
from PyInquirer import prompt, print_json
from Repositories import Repositories
from PublicRepos import PublicRepos
import sys


class Options:

    def __init__(self, uName, uToken):
        self.options = ['Work with your repositories',
                        'List a users public repos', 'Create a repo', 'Exit']
        self.userChoice = ""
        self.userName = uName
        self.token = uToken
        self.listOptions()

    def listOptions(self):
        questions = [
            {'type': 'list', 'name': 'options',
                'message': 'What would you like to do?', 'choices': self.options}
        ]
        self.userChoice = prompt(questions)
        if (self.userChoice['options'] == 'Work with your repositories'):
            reposObject = Repositories('change', self.userName, self.token)
        elif (self.userChoice['options'] == 'List a users public repos'):
            pReposObject = PublicRepos()
        elif (self.userChoice['options'] == 'Create a repo'):
            reposObject = Repositories('create', self.userName, self.token)
        else:
            sys.exit()
