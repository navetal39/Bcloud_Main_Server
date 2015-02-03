# INFO: #
# First version.
# No Encryption.
# ===================================


def decrypt(data):
    '''Will be implimented. At some point...
    '''
    return data

def start_run():
    '''A method that runs when you first run the server.
    '''
    database_file=open('database.txt', 'r')
    encrypted_database_content = database_file.read()
    database_content=decrypt(encrypted_database_content)
    database_lines=database_content.split('\n')
    global dict_database
    dict_database={}
    for line in database_lines:
        if line!="":
            name, password=line.split(':')
            dict_database[name]=password
    database_file.close()

def name_exists(name):
    '''This method returns True if the name is already occupied, and false Otherwise
    '''
    return name in dict_database.keys()

def register_new_user(username, password):
    '''Registers a new user... Duh.
    '''
    if name_exists(username):
        return 'Name_Exists'
    else:
        dict_database[username]=password
        database=open('database.txt', 'a')
        print >>database, '{n}:{p}'.format(n=username, p=password)
        database.close()

def authenticate(name, password):
    '''Returns True if the name and password matches, and False otherwise
    '''
    return name_exists(name) and dict_database[name]==password

try:
    dict_database[0]
except:
    start_run()

'''
Exciting. Satisfying. Period.
.
'''
