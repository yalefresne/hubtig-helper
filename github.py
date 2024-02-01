import getpass
import logging

from typing import Tuple

import api
import utils

from settings import Settings


class Github:
    __instance = None

    api_url = 'https://api.github.com'
    token_url = 'https://github.com/settings/tokens'

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = Github()
        return cls.__instance

    def __init__(self):
        self.context_count = 0
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        self.context_count += 1

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.context_count -= 1

    @property
    def org_url(self) -> str:
        with Settings() as settings:
            return f'{self.api_url}/orgs/{settings.github_org}'

    @property
    def header(self) -> Tuple:
        with Settings() as settings:
            return {
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {settings.github_token}',
                'X-GitHub-Api-Version': '2022-11-28',
                }

    def listPackages(self, type: str = 'container'):
        url = f'{self.org_url}/packages?package_type={type}'
        return api.get(url, self.header)

    def listVersions(self, package: str):
        url = f'{self.org_url}/packages/container/{package}/versions?per_page=100'
        return api.get(url, self.header)

    def deleteVersion(self, package: str, version_id: str) -> None:
        url = f'{self.org_url}/packages/container/{package}/versions/{version_id}'
        return api.delete(url, self.header)

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
