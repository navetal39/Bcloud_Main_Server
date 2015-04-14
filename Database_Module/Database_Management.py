# -*- coding: cp1255 -*-
# INFO: #
# No Encryption.
# ===================================

import socket, sys
sys.path.append('../')
import crypto # Check about its path - Tamir

class DataBase(object):
    def __init__(self, ip, port):
        ''' This method will run every time you boot up the module.
        '''
        self.MEMORY_IP = ip
        self.MEMORY_PORT = port
        self.MEMORY_SOCKET = socket.socket()
        self.dict_database = {}
        
        database_file = open('database.txt', 'r')
        encrypted_database_content = database_file.read()
        encrypted_lines = encrypted_database_content.split('§§§')
        for encrypted_line in encrypted_lines:
            line = crypto.decrypt(encrypted_line)
            if line != "":
                name, password = line.split(':')
                self.dict_database[name] = password
        database_file.close()

    def __str__(self):
        info = ''
        for key in self.dict_database.keys():
            info += "{name}: {pw}\n".format(name=key, pw=self.dict_database[key])
        return info
    
    def __repr__(self):
        info = ''
        for key in self.dict_database.keys():
            info += "{name}:{pw}\n".format(name=key, pw=self.dict_database[key])
        return info

    def connect(self):
        self.MEMORY_SOCKET = socket.socket()
        self.MEMORY_SOCKET.connect((self.MEMORY_IP, self.MEMORY_PORT))

    def disconnect(self):
        self.MEMORY_SOCKET.close()

    def make_folder(self, name):
        ''' This method is dedicated to communicating with the Storage module for setting up new directories.
        '''
        try:
            message = "MNF|" + name
            self.connect()
            self.MEMORY_SOCKET.send(message)
            response = self.MEMORY_SOCKET.recv(5000)
            self.disconnect()
            message_parts = message.split('|')
            response_parts = response.split('|')
            flag = response_parts[0]; response_parts.remove(flag)
            if response_parts == message_parts:
                return flag
            else:
                raise
        except Exception, e:
            print 'error: '+e
            return "WTF"

    def name_exists(self, name):
        ''' Verifies that a given name exists in the database
        '''
        try:
            if name in self.dict_database.keys():
                return "SCS"
            else:
                return "NNM"
        except:
            return "WTF"

    def register_new_user(self, username, password):
        ''' A method for registering new users.
        '''
        try:
            if self.name_exists(username) == "SCS":
                return 'NIU'
            elif self.name_exists(username) == "NNM":
                self.dict_database[username] = password
                database = open('database.txt', 'a')
                encrypted_data = crypto.encrypt('{n}:{p}'.format(n=username, p=password))
                print >>database, encrypted_data+'§§§'
                database.close()
                return self.make_folder(username)
            else:
                raise
        except:
            return "WTF"

    def authenticate(self, name, password):
        ''' Verifies that a given name and a given password matches in the database
        '''
        try:
            if self.name_exists(name):
                if self.dict_database[name] == password:
                    return "SCS"
                else:
                    return "NPW"
            else:
                return "NNM"
        except:
            return "WTF"

'''
Exciting. Satisfying. Period.
.
'''
