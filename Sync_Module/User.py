# Info: #
# ===================================

import sys, socket
sys.path.append('../')
from COM import *
from RECURRING_FUNCTIONS import file_send, file_recv


class User(object):
    def __init__(self, username):
        self.username = username
        self.sock=socket.socket()
        
    def __str__(self):
        return "A user named {}".format(self.username)
    def __repr__(self):
        return "User:{}".format(self.username)

    def connect(self, module):
        self.sock=socket.socket()
        if module == 'memory':
            self.sock.connect((MEMORY_IP, MEMORY_PORT))
        elif module == 'database':
            self.sock.connect((DATABASE_IP, DATABASE_PORT))
        else: # Just so there'll be an else
            pass

    def disconnect(self):
        self.sock.close()

    def authenticate(self, password):
        try:
            self.connect('database')
            message = 'AUT|{}|{}'.format(self.username, password)
            self.sock.send(message)
            response = self.sock.recv(5000)
            self.disconnect()
            response_parts = response.split('|')
            flag = response_parts[0]; response_parts.remove(flag)
            if response_parts == message.split('|'):
                return flag
            else:
                raise
        except:
            return 'WTF'
    
    def get_folder_info(self, folder_type):
        try:
            self.connect('memory')
            message = 'LUD|{}|{}'.format(self.username, folder_type)
            self.sock.send(message)
            response = file_recv(self.sock)
            self.disconnect()
            return 'SCS', response
        except:
            return 'WTF', 'WTF'

    def set_folder_info(self, folder_type, data):
        try:
            self.connect('memory')
            message = 'NUD|{}|{}'.format(self.username, folder_type)
            self.sock.send(message)
            response = self.sock.recv(5000)
            response_parts = response.split('|')
            flag = response_parts[0]; response_parts.remove(flag)
            if flag == 'ACK' and response_parts == message.split('|'):
                file_send(self.sock, data)
                final_response = self.sock.recv(5000)
                self.disconnect()
                final_response_parts = final_response.split('|')
                final_flag = final_response_parts[0]; final_response_parts.remove(final_flag)
                if final_response_parts == message.split('|'):
                    return final_flag
                else:
                    raise
            else:
                raise
        except:
            try:
                self.disconnect()
            except:
                pass # If it didn't manage do disconnect, then it was already closed.
            return 'WTF'
        
    def get_files(self, folder_type, file_list):
        try:
            self.connect('memory')
            files = file_list[0]; file_list.remove(files) # There's at least one file
            for file_name in file_list: # If there's more than one file
                files+='|{}'.format(file_name)
            self.sock.send('FLS|{}|{}|{}'.format(self.username, folder_type, files))
            data = file_recv(self.sock)
            self.disconnect()
            return 'SCS', data
        except:
            return 'WTF', 'WTF'
        
    def update_folder(self, folder_type, data):
        try:
            self.connect('memory')
            message = 'WRT|{}|{}'.format(self.username, foler_type)
            self.sock.send(message)
            response = self.recv(5000)
            response_parts = respnse.split('|')
            flag = response_parts[0]; response_parts.remove(flag)
            if flag == 'ACK' and response_parts == message.split('|'):
                file_send(self.sock, data)
                self.disconnect()
                return 'SCS'
            else:
                raise
        except:
            self.disconnect()
            return 'WTF'

    def delete_file(self, folder_type, file_name):
        try:
            self.connect('memory')
            self.sock.send('DEL|{}|{}|{}'.format(self.username, folder_type, file_name))
            response = self.sock.recv(5000)
            self.disconnect()
            response_parts = respnse.split('|')
            flag = response_parts[0]; response_parts.remove(flag)
            if response_parts == message.split('|'):
                return flag
            else:
                raise
        except:
            return 'WTF'

'''
Exciting. Satisfying. Period.
.
'''
