import os

MAIN_PATH = os.getcwd()
print(MAIN_PATH)

def get_scripts(path):
    '''
    Imports scripting file (default to .sql for now) and creates dictionary to be used as an extraction form
    '''
    sqls = {}
    for name in os.listdir(path):
        if name.endswith('sql'):
            with open(os.path.join(path, name), 'r') as f:
                script = f.read()
            sqls.update({name: script})
    return sqls