import os

from dotenv import dotenv_values


class Settings:
    default_env_vars = [
            'GITHUB_TOKEN',
            'GITHUB_ORG',
            ]

    def __init__(self):
        if not os.path.isfile('.env'):
            open('.env', 'x')

        config = dotenv_values('.env')

        for var in self.default_env_vars:
            if var in config:
                setattr(self, var.lower(), config[var])
