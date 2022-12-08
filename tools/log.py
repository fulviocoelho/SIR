import os

def log(*arg):
    if 'VERBOSE' in os.environ and eval(os.environ['VERBOSE']) == True:
        print(*arg)