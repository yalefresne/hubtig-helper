import getpass

import utils


class Github:
    token_url = 'https://github.com/settings/tokens'

    def askGithubToken(self) -> str:
        return getpass.getpass('Enter your github token: ')

    def updateGithubToken(self) -> str:
        github_token = self.askGithubToken()
        utils.updateEnvFile('GITHUB_TOKEN', github_token)

        return github_token

    def askGithubOrganization(self) -> str:
        return input('Enter your github organization: ')

    def updateGithubOrg(self) -> str:
        github_organization = self.askGithubOrganization()
        utils.updateEnvFile('GITHUB_ORG', github_organization)

        return github_organization
