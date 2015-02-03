# INFO: #
# First version.
# No Encryption.
# ===================================

import socket
MEMORY_IP='0.0.0.0'
MEMORY_PORT=9077
MEMORY_SOCKET=socket.socket()

def Start_Run():
    '''This method will run every time you boot up the module.
    '''
    MEMORY_SOCKET.connect((MEMORY_IP, MEMORY_PORT))
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

def Decrypt(data):
    '''Decrypts the data it gets. Unimplimented.
    '''
    return data

def Make_Folder(name):
    '''This method is dedicated to communicating with the Storage module for setting up new directories.
    '''
    try:
        MEMORY_SOCKET.send("Make;"+name)
        response=MEMORY_SOCKET.recv(1024)
        return response
    except:
        return "Unknown error"

def Name_Exists(name):
    '''Verifies that a given name exists in the database
    '''
    try:
        if name in dict_database.keys():
            return "Success"
        else:
            return "Unknown name"
    except:
        return "Unknown error"

def Register_New_User(username, password):
    '''A method for registering new users.
    '''
    try:
        if Name_Exists(username):
            return 'Name in use'
        else:
            dict_database[username]=password
            database=open('database.txt', 'a')
            print >>database, '{n}:{p}'.format(n=username, p=password)
            database.close()
            return Make_Folder(name)
    except:
        return "Unknown error"

def Authenticate(name, password):
    '''Verifies that a given name and a given password matches in the database
    '''
    try:
        if Name_Exists(name):
            if dict_database[name]==password:
                return "Success"
            else:
                return "Authentication Failed"
        else:
            return "Unknown name"
    except:
        return "Unknown error"


try:
    dict_database[0]
except:
    Start_Run()

'''
Exciting. Satisfying. Period.
.
'''
