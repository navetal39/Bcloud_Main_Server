# INFO: #
# First version.
# No Encryption.
# ===================================

import socket

class DataBase(object):
    def __init__(self):
        ''' This method will run every time you boot up the module.
        '''
        #MEMORY_IP = '0.0.0.0'
        #MEMORY_PORT = 9077
        #self.MEMORY_SOCKET = socket.socket()
        #self.MEMORY_SOCKET.connect((MEMORY_IP, MEMORY_PORT))
        self.dict_database = dict()
        
        database_file = open('database.txt', 'r')
        encrypted_database_content = database_file.read()
        database_content = self.decrypt(encrypted_database_content)
        database_lines = database_content.split('\n')
        for line in database_lines:
            if line != "":
                name, password = line.split(':')
                self.dict_database[name] = password
        database_file.close()

    def __str__(self):
        info=''
        for key in self.dict_database.keys():
            info+="{name}: {pw}; ".format(name=key, pw=self.dict_database[key])
        return info
    
    def __repr__(self):
        info=''
        for key in self.dict_database.keys():
            info+="{name}: {pw}\n".format(name=key, pw=self.dict_database[key])
        return info

    def decrypt(self, data):
        ''' Decrypts the data it gets. Unimplimented.
        '''
        return data

    def make_folder(self, name):
        ''' This method is dedicated to communicating with the Storage module for setting up new directories.
        '''
        try:
            self.MEMORY_SOCKET.send("Make;" + name)
            response = self.MEMORY_SOCKET.recv(1024) # deal with recieving a full response... thing with leangth, if needed.
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
            if self.name_exists(username) == "Success":
                return 'Name in use'
            elif self.name_exists(username) == "Unknown name":
                self.dict_database[username] = password
                database = open('database.txt', 'a')
                print >>database, '{n}:{p}'.format(n=username, p=password)
                database.close()
                #return make_folder(name)
            else:
                raise
        except:
            return "Unknown error"

    def authenticate(self, name, password):
        ''' Verifies that a given name and a given password matches in the database
        '''
        try:
            if self.name_exists(name):
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
