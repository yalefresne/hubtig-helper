import json
import os
import tempfile


ANSWER_YES = 'yes'
ANSWER_NO = 'no'
ANSWER_ALL = 'all'
ANSWER_QUIT = 'quit'


def yesNoQuestion(question: str) -> bool:
    yes_answer = ['yes', 'y', 'Yes', 'YES', 'Y', '']

    answer = input('{} ? y/n [yes]: '.format(question))
    if answer in str(yes_answer):
        return True

    return False


def yesNoWithOptionsQuestion(question: str) -> str:
    yes_answer = ['yes', 'y', 'Yes', 'YES', 'Y`', '']
    no_answer = ['no', 'n', 'No', 'NO', 'N']
    all_answer = ['all', 'a', 'All', 'ALL', 'A']
    quit_answer = ['quit', 'q', 'Quit', 'QUIT', 'Q']

    answer = input(f'{question} ? y/n/q/a [yes]: ')
    if answer in str(yes_answer):
        return ANSWER_YES
    if answer in str(no_answer):
        return ANSWER_NO
    if answer in str(all_answer):
        return ANSWER_ALL
    if answer in str(quit_answer):
        return ANSWER_QUIT

    ask_question_again_prefix = 'Bad format answer: '
    question_clean = question.removeprefix(ask_question_again_prefix)
    yesNoWithOptionsQuestion(f'Bad format answer: {question_clean}')


def updateEnvFile(var: str, value: str):
    """
    It is not optimized but .env file is small for now
    If file grow up we will thinking about optimization
    """
    file = '.env'
    old_env = open(file)
    var_in_file = False
    with tempfile.NamedTemporaryFile(dir=os.path.dirname(file)) as new_file:
        for line in old_env:
            if var in line:
                var_in_file = True
                new_file.write(bytes('{}={}\n'.format(var, value), 'utf8'))
                continue

            new_file.write(bytes(line, 'utf8'))

        if not var_in_file:
            new_file.write(bytes('{}={}\n'.format(var, value), 'utf8'))

        old_env.close()
        os.remove(file)
        os.link(new_file.name, file)


def underscore_to_camelcase(value):
    """
    It is not a real camelCase cause the first letter will be upper
    e.g: GITHUB_TOKEN becomes GithubToken
    """
    temp = value.split('_')
    return ''.join(elem.title() for elem in temp)


def save_json(name: str, data) -> None:
    json_folder = 'json'
    # Serializing json
    json_object = json.dumps(data, indent=4)

    file = open(f'{json_folder}/{name}.json', 'w', encoding='utf8')
    file.write(json_object)
    file.close()


def beautyPrint(desc: str, delimiter: str = '-', newline: bool = True):
    desc = ' ' + desc + ' '
    desc = desc.title().center(60, delimiter)
    if newline:
        desc = '\n' + desc + '\n'
    print(desc)
