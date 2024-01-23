#!/usr/bin/python3
import argparse
import os
import sys
import webbrowser

from datetime import datetime
from pyfiglet import Figlet
from typing import Tuple

# Project's module
import utils

from github import Github
from settings import Settings


parser = argparse.ArgumentParser(
        prog='packclean',
        description='Clean your packages Github.'
        )

parser.add_argument(
        '-c',
        '--config',
        help='Configure this tool interactively.',
        action='store_true',
        )

parser.add_argument(
        '-ls',
        '--list',
        help='List organization\'s packages.',
        action='store_true',
        )

parser.add_argument(
        '-p',
        '--package',
        help='List package\'s versions.',
        type=str,
        )

parser.add_argument(
        '--untagged',
        help='Remove untagged package\'s versions.',
        type=str,
        metavar='PACKAGE',
        )

parser.add_argument(
        '--json',
        help='Save result in a json file.',
        action='store_true',
        )

parser.add_argument(
        '-y',
        '--yes',
        help='Don\'t ask for confirmation.',
        action='store_true',
        )

parser.add_argument(
        '-a',
        '--all',
        help='Action as effect on all elements.',
        action='store_true',
        )

parser.add_argument(
        '--dry-run',
        help='Action as no effect, just print what will be done.',
        action='store_true',
        )


def configure(all_mode: bool = False, dry_run_mode: bool = False) -> Tuple:
    utils.beautyPrint('configuration')
    settings = Settings()
    github = Github()

    config = {}
    for param in settings.default_env_vars:
        snake_param = utils.underscore_to_camelcase(param)
        elem_param = param.split('_')[1].lower()

        if hasattr(github, f'update{snake_param}'):
            updateParam = getattr(github, f'update{snake_param}')

        if hasattr(settings, param.lower()) and getattr(settings, param.lower()):
            if all_mode or utils.yesNoQuestion(f'Do you want to update {param}'):
                config[elem_param] = updateParam()
            else:
                config[elem_param] = getattr(settings, param.lower())
        else:
            if 'GITHUB_TOKEN' == param and not utils.yesNoQuestion('Have you github token with read package/write permission'):
                webbrowser.open_new_tab(github.token_url)

            config[elem_param] = updateParam()

    return config


def listPackage(save_mode: bool = False):
    utils.beautyPrint('packages list')
    with Github() as gh:
        packages = gh.listPackages()

    if save_mode:
        utils.save_json('packages_list', packages)

    for package in packages:
        print(package['name'])


def packageVersions(package: str, save_mode: bool = False) -> None:
    utils.beautyPrint(f'{package} versions list')
    with Github() as gh:
        versions = gh.listVersions(package)
    if save_mode:
        utils.save_json(f'{package}_versions_list', versions)

    for version in versions:
        created_at = datetime.strptime(version['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        print(created_at,
              version['html_url'],
              version['metadata']['container']['tags']
              )


def deleteUntaggedVersion(
        package: str,
        version_id: str,
        dry_run_mode: bool = False,
        ) -> int:
    with Github() as gh:
        if not dry_run_mode:
            response = gh.deleteVersion(package, version_id)

    if dry_run_mode or response and response.status_code == 204:
        print(f'Package version {version_id} deleted')
        return 1
    else:
        print('Error during process')
        print(response)
        return 0


def deleteUntaggedVersions(
        package: str,
        all_mode: bool = False,
        dry_run_mode: bool = False,
        save_mode: bool = False
        ) -> None:
    count_deleted = 0
    count_total = 0

    utils.beautyPrint(f'Delete untagged {package} versions')
    with Github() as gh:
        versions = gh.listVersions(package)

        for version in versions:
            created_at = datetime.strptime(version['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            tags = version['metadata']['container']['tags']
            version_id = version['id']

            if not tags:
                count_total += 1
                print(created_at, version['html_url'])

                if save_mode:
                    utils.save_json(f"{package}_{version_id}_untagged", version)

                if all_mode:
                    count_deleted += deleteUntaggedVersion(package, version_id, dry_run_mode)
                    continue

                user_answer = utils.yesNoWithOptionsQuestion(f'Confirm deletion version {version_id}')
                if user_answer == utils.ANSWER_YES:
                    count_deleted += deleteUntaggedVersion(package, version_id, dry_run_mode)
                elif user_answer == utils.ANSWER_ALL:
                    count_deleted += deleteUntaggedVersion(package, version_id, dry_run_mode)
                    all_mode = True
                elif user_answer == utils.ANSWER_QUIT:
                    sys.exit(1)

        print(f'Deleted versions: {count_deleted}/{count_total}')


args = parser.parse_args()

if 1 == len(sys.argv):
    f = Figlet(font='slant')
    print(f.renderText('packclean'))
    parser.print_help()
    parser.exit(0)

dry_run_mode = True if args.dry_run else False
not_confirm = True if args.yes or args.all else False
save_mode = True if args.json else False

if dry_run_mode:
    print('Dry run mode: Action as no effect, just print what will be done.')
if save_mode:
    print('Save result in a json file.')
try:
    if args.config:
        configure(
                not_confirm,
                dry_run_mode,
                )
    if args.list:
        listPackage(
                save_mode
                )
    if args.package:
        packageVersions(
                args.package,
                save_mode
                )
    if args.untagged:
        deleteUntaggedVersions(
                args.untagged,
                not_confirm,
                dry_run_mode,
                save_mode
                )
except KeyboardInterrupt:
    print('\nInterrupted')
    try:
        parser.exit(130)
    except SystemExit:
        os._exit(130)

parser.exit(1)
