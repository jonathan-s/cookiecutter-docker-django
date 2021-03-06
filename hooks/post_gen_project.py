import os
import random
import string
import urllib.request

def remove_files(*file_names):
    for i in file_names:
        os.remove(i)

def generate_random_string(
    length,
    digits = True,
    ascii_letters = True,
    punctuation = False
):
    symbols = []
    if digits:
        symbols += string.digits
    if ascii_letters:
        symbols += string.ascii_letters
    if punctuation:
        all_punctuation = set(string.punctuation)
        exclude = {"'", '"', '\\', '$', '/'}
        suitable = all_punctuation.difference(exclude)
        symbols += ''.join(suitable)
    return ''.join([random.choice(symbols) for i in range(length)])

def set_flag(file_path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your system. "
                "Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value

def main():
    if "{{ cookiecutter.license }}" ==  "Not open source":
        remove_files('LICENSE')

    #
    # .gitlab-ci.yml
    #

    # Set random database user
    set_flag(
        '.gitlab-ci.yml',
        'CC_DB_USER_CC',
        length=24,
    )

    # Set random password for database user password
    set_flag(
        '.gitlab-ci.yml',
        'CC_DB_PASS_CC',
        length=24,
    )

    # Set random database
    set_flag(
        '.gitlab-ci.yml',
        'CC_DB_CC',
        length=32,
    )

    if "{{ cookiecutter.use_docker }}".lower() == "n":
        remove_files('docker-compose.yml', '.dockerignore', 'Dockerfile', 'docker-entrypoint.sh')

    #
    # .env file
    #

    # Set secret Key
    set_flag(
        '.env',
        'CC_SECRET_KEY_CC',
        length=50,
        punctuation=True,
    )

    # Set random database user
    set_flag(
        '.env',
        'CC_DB_USER_CC',
        length=24,
    )

    # Set random password for database user password
    set_flag(
        '.env',
        'CC_DB_PASS_CC',
        length=24,
    )

    # Set random database
    set_flag(
        '.env',
        'CC_DB_CC',
        length=32,
    )

    #
    # settings.py file
    #

    # Set development secret key at settings.py
    set_flag(
        'config/settings/common.py',
        'CC_SECRET_KEY_CC',
        length=50,
        punctuation=True,
    )

if __name__ == "__main__":
    main()
