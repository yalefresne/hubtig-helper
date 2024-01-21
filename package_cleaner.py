#!/usr/bin/python3
import argparse
import os
import sys
import webbrowser

from typing import Tuple

# Project's module
import utils

from github import Github
from settings import Settings


parser = argparse.ArgumentParser(
        prog='packclean',
        description='Clean your packages Github'
        )

parser.add_argument(
        '-c',
        '--config',
        help='Configure this tool interactively',
        action='store_true',
        )

args = parser.parse_args()


def configure() -> Tuple:
    settings = Settings()
    github = Github()

    config = {}
    for param in settings.default_env_vars:
        snake_param = utils.underscore_to_camelcase(param)
        elem_param = param.split('_')[1].lower()

        if hasattr(github, f'update{snake_param}'):
            updateParam = getattr(github, f'update{snake_param}')

        if hasattr(settings, param.lower()) and getattr(settings, param.lower()):
            if utils.yesNoQuestion(f'Do you want to update {param}'):
                config[elem_param] = updateParam()
            else:
                config[elem_param] = getattr(settings, param.lower())
        else:
            if 'GITHUB_TOKEN' == param and not utils.yesNoQuestion('Have you github token with read package/write permission'):
                webbrowser.open_new_tab(github.token_url)

            config[elem_param] = updateParam()

    return config


def run_command(command: str):
    try:
        command()
    except KeyboardInterrupt:
        print('\nInterrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
    sys.exit(1)


if args.config:
    run_command(configure)

parser.print_help()
