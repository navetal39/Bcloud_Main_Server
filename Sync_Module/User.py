# Info: #
# ===================================

import sys, socket
sys.path.append('../')
from COM import *
from RECURRING_FUNCTIONS import file_recv


class User(object):
    def __init__(self, username):
        self.username = username
        self.sock=socket.socket()
        
    def __str__(self):
        return "A user named {}".format(self.username)
    def __repr__(self):
        return "User:{}".format(self.username)

    def connect(self, module):
        if module = 'memory':
            self.sock.connect((MEMORY_IP, MEMORY_PORT))
        elif module = 'database':
            self.sock.connect((DATABASE_IP, DATABASE_PORT))
        else: # Just so there'll be an else
            pass

    def authenticate(self, username, password):
        self.connect('database')
        message = 'AUT;{};{}'.format(username, password)
        self.sock.send(message)
        response = self.sock.recv(5000)
        self.disconnect()
        response_parts = response.split(';')
        flag = response_parts[0]; response_parts.remove(flag)
        if response_parts = message.split(';'):
            return flag
        else:
            return 'WTF'

    def disconnect(self):
        self.sock.close()
    
    def get_folder_info(self, folder_type):
        pass
        
    def set_folder_info(self, folder_type, info):
        pass
        
    def get_file(self, folder_type, file_name):
        pass
        
    def write_to_file(self, folder_type, file_name, data):
        pass


'''
Exciting. Satisfying. Period.
.
'''
