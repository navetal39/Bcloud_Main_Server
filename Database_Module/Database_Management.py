# INFO: #
# First version.
# No Encryption.
# ===================================


def Decrypt(data):
    '''Will be implimented. At some point...
    '''
    return data

def Start_Run():
    '''A method that runs when you first run the server.
    '''
    database_file=open('database.txt', 'r')
    encrypted_database_content = database_file.read()
    database_content=Decrypt(encrypted_database_content)
    database_lines=database_content.split('\n')
    global dict_database
    dict_database={}
    for line in database_lines:
        if line!="":
            name, password=line.split(':')
            dict_database[name]=password
    database_file.close()

def Name_Exists(name):
    '''This method returns True if the name is already occupied, and false Otherwise
    '''
    return name in dict_database.keys()

def Register_New_User(username, password):
    '''Registers a new user... Duh.
    '''
    if Name_Exists(username):
        return 'Name_Exists'
    else:
        dict_database[username]=password
        database=open('database.txt', 'a')
        print >>database, '{n}:{p}'.format(n=username, p=password)
        database.close()

def Authenticate(name, password):
    '''Returns True if the name and password matches, and False otherwise
    '''
    return Name_Exists(name) and dict_database[name]==password

try:
    dict_database[0]
except:
    Start_run()

'''
Exciting. Satisfying. Period.
.
'''
