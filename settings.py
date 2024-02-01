import logging
import os

from dotenv import dotenv_values


class Settings:
    __instance = None

    default_env_vars = [
            'GITHUB_TOKEN',
            'GITHUB_ORG',
            ]

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = Settings()
        return cls.__instance

    def __init__(self):
        self.context_count = 0
        self.logger = logging.getLogger(__name__)

        if not os.path.isfile('.env'):
            open('.env', 'x')

        config = dotenv_values('.env')

        for var in self.default_env_vars:
            if var in config:
                setattr(self, var.lower(), config[var])

    def __enter__(self):
        self.context_count += 1

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.context_count -= 1
