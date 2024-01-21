import os
import tempfile


def yesNoQuestion(question: str) -> bool:
    yes_answer = ['yes', 'y', 'Yes', 'YES', 'Y', '']

    answer = input('{} ? y/n [yes]: '.format(question))
    if answer in str(yes_answer):
        return True

    return False


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
