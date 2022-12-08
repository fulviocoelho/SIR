import os
import sys
import yaml
import json
import emoji
from termcolor import colored

def load_configs():
    EXT = ['yaml', 'yml', 'json']
    for ext in EXT:
        if os.path.isfile(f'./config.{ext}'):
            if ext in ['yaml', 'yml']:
                with open(f'config.{ext}', 'r') as file:
                    return yaml.safe_load(file)
            else:    
                return json.load(open('config.json'))
    return None

def find_parameter_value(parameter):
    try:
        return sys.argv[sys.argv.index(parameter)+1]
    except:
        print(f'parameter value not found ({parameter})')
        exit()

def run_tests(TESTS = []):
    tests = [x.split('.')[0] for x in os.listdir() if '.py' in x]
    for test in tests:
        if os.system(f'{os.environ["PYTHON"]} {test}.py') == 0:
            TESTS.append({ "test": test, "status": "PASS" })
            print(emoji.emojize(f'  :green_circle: {colored(f"{test}: PASS", "green")}'))
        else:
            TESTS.append({ "test": test, "status": "FAIL" })
            print(emoji.emojize(f'  :red_circle: {colored(f"{test}: FAIL", "red")}'))

def run_tests_in_folders(BASE_PATH, FOLDERS = []):
    tests_folders = [x for x in os.listdir() if '.' not in x]
    for folder in tests_folders:
        os.chdir(f'{BASE_PATH}/{folder}')
        FOLDERS.append({ "folder": folder, "tests": [] })
        print(emoji.emojize(f':open_file_folder: {colored(f"{folder}", "yellow")}'))
        run_tests(FOLDERS[len(FOLDERS)-1]['tests'])

def main():    
    OUTPUT_FORMAT = None
    PROFILE = None
    VERBOSE = None
    if '--output' in sys.argv:
        OUTPUT_FORMAT = find_parameter_value('--output')
    if '--profile' in sys.argv:
        PROFILE = find_parameter_value('--profile')
    if '--verbose' in sys.argv:
        VERBOSE = find_parameter_value('--verbose')

    if VERBOSE is not None and VERBOSE.lower() == 'true':
        os.environ['VERBOSE'] = 'True'

    CONFIG = load_configs()
    OUTPUT_FORMATS = ['json', 'csv']
    BASE_TEST_FOLDER = f'tests'
    TESTS = []
    FOLDERS = []
    if CONFIG is not None:
        if 'profiles' in CONFIG:
            if PROFILE is not None:
                try:
                    BASE_TEST_FOLDER = f'/{CONFIG["profiles"][PROFILE]}'
                except:
                    print('Profile not found')
                    exit()
            elif 'default' in CONFIG['profiles']:
                BASE_TEST_FOLDER = f'/{CONFIG["profiles"]["default"]}'
    BASE_PATH = f'{os.getcwd()}/{BASE_TEST_FOLDER}'
    APP_PATH = f'{os.getcwd()}'
    
    os.environ['APP_PATH'] = APP_PATH

    if OUTPUT_FORMAT is not None and OUTPUT_FORMAT not in OUTPUT_FORMATS:
        print(f'output format should be {OUTPUT_FORMATS[0]} or {OUTPUT_FORMATS[1]}')
        exit()

    os.chdir(BASE_PATH)

    run_tests(TESTS)
    run_tests_in_folders(BASE_PATH, FOLDERS)

    if len(TESTS) > 0:
        FOLDERS.append({ "folder": "root", "tests": TESTS })

    os.chdir(APP_PATH)

    if OUTPUT_FORMAT is not None:
        FILE_NAME = ''
        if PROFILE is not None:
            FILE_NAME = f'{PROFILE}_output'
        else:
            FILE_NAME = f'output'

        if OUTPUT_FORMAT == 'csv':
            with open(f'./{FILE_NAME}.csv', 'w', encoding='utf8') as f:
                f.write(f'folder,test,status\n')
                for folder in FOLDERS:
                    for test in folder['tests']:
                        f.write(f'{folder["folder"]},{test["test"]},{test["status"]}\n')
        else:
            with open(f'./{FILE_NAME}.json', 'w', encoding='utf8') as f:
                f.write(json.dumps(FOLDERS, indent=2))

main()