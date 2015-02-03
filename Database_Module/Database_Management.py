# INFO: #
# First version.
# No Encryption.
# ===================================

import socket
MEMORY_IP='0.0.0.0'
MEMORY_PORT=9077
MEMORY_SOCKET=socket.socket()

def Decrypt(data):
    return data

def Make_Folder(name):
    try:
        MEMORY_SOCKET.send("Make;"+name)
        response=MEMORY_SOCKET.recv(1024)
        return response
    except:
        return "Unknown error"

def Start_Run():
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

def Name_Exists(name):
    try:
        if name in dict_database.keys():
            return "Success"
        else:
            return "Unknown name"
    except:
        return "Unknown error"

def Register_New_User(username, password):
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
