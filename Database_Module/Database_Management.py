# INFO: #
# First version.
# No Encryption.
# ===================================

import socket

class DataBase(object):
    def __init__():
        ''' This method will run every time you boot up the module.
        '''
        MEMORY_IP = '0.0.0.0'
        MEMORY_PORT = 9077
        self.MEMORY_SOCKET = socket.socket()
        self.MEMORY_SOCKET.connect((MEMORY_IP, MEMORY_PORT))
        self.dict_database = dict(self)
        
        database_file = open('database.txt', 'r')
        encrypted_database_content = database_file.read()
        database_content = decrypt(encrypted_database_content)
        database_lines = database_content.split('\n')
        for line in database_lines:
            if line != "":
                name, password = line.split(':')
                self.dict_database[name] = password
        database_file.close()


    def decrypt(self, data):
        ''' Decrypts the data it gets. Unimplimented.
        '''
        return data

    def make_folder(self, name):
        ''' This method is dedicated to communicating with the Storage module for setting up new directories.
        '''
        try:
            self.MEMORY_SOCKET.send("Make;" + name)
            response = MEMORY_SOCKET.recv(1024) # deal with recieving a full response... thing with leangth, if needed.
            return response
        except:
            return "Unknown error"

    def name_exists(self, name):
        ''' Verifies that a given name exists in the database
        '''
        try:
            if name in self.dict_database.keys():
                return "Success"
            else:
                return "Unknown name"
        except:
            return "Unknown error"

    def register_new_user(self, username, password):
        ''' A method for registering new users.
        '''
        try:
            if name_exists(username) == "Success":
                return 'Name in use'
            elif name_exists(username) == "Unknown name":
                self.dict_database[username] = password
                database = open('database.txt', 'a')
                print >>database, '{n}:{p}'.format(n=username, p=password)
                database.close()
                return make_folder(name)
            else:
                raise
        except:
            return "Unknown error"

    def authenticate(self, name, password):
        ''' Verifies that a given name and a given password matches in the database
        '''
        try:
            if name_exists(name):
                if self.dict_database[name] == password:
                    return "Success"
                else:
                    return "Authentication Failed"
            else:
                return "Unknown name"
        except:
            return "Unknown error"

'''
Exciting. Satisfying. Period.
.
'''
