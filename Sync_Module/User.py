# Info: #
# ===================================

import sys, socket
sys.path.append('../')
from COM import *
from RECURRING_FUNCTIONS import file_send, file_recv


class User(object):
    def __init__(self, username):
        ''' Creates a new user object, which will be used to forward requests that the actual user sends.
        '''
        self.username = username
        self.sock = socket.socket()
        
    def __str__(self): # Used for debug
        return "A user named {}".format(self.username)
    def __repr__(self): # Used for debug
        return "User:{}".format(self.username)

    def connect(self, module):
        ''' Connects to the given module, used to allow quick and easy connections.
        '''
        self.sock=socket.socket()
        if module == 'memory':
            self.sock.connect((MEMORY_IP, MEMORY_PORT))
        elif module == 'database':
            self.sock.connect((DATABASE_IP, DATABASE_PORT))
        else: # Just so there'll be an else
            pass

    def disconnect(self):
        ''' Disconnects from whichever module it was connected to
        '''
        self.sock.close()

    def authenticate(self, password):
        ''' Authenticates using self's username and the given password with the help of the database module.
        '''
        try:
            self.connect('database')
            print 'aut: connected'
            message = 'AUT|{}|{}'.format(self.username, password)
            print 'aut: made message'
            self.sock.send(message)
            print 'aut: sent'
            response = self.sock.recv(len(message) + 5)
            print 'aut: recived'
            self.disconnect()
            print 'aut: disconnected'
            response_parts = response.split('|')
            print 'aut: parts'
            flag = response_parts[0]; response_parts.remove(flag)
            print 'aut: flag'
            if response_parts == message.split('|'):
                return flag
            else:
                raise
        except Exception, error:
            print 'ERROR', error
            return 'WTF'
    
    def get_folder_info(self, folder_type):
        ''' Gets the folder info from the memory module.
        '''
        try:
            self.connect('memory')
            print 'gfi: connected'
            message = 'LUD|{}|{}'.format(self.username, folder_type)
            print 'gfi: made message'
            self.sock.send(message)
            print 'gfi: sent'
            response = file_recv(self.sock)
            print 'gfi: recived'
            self.disconnect()
            print 'gfi: disconnected'
            return 'SCS', response
        except Exception, error:
            print 'ERROR', error
            return 'WTF', 'WTF'

    def set_folder_info(self, folder_type, data):
        ''' Sends a request to the memory module to update the folder info
        '''
        try:
            # First step - set up connection
            self.connect('memory')
            print 'sfi: connceted'
            message = 'NUD|{}|{}'.format(self.username, folder_type)
            print 'sfi: made message'
            self.sock.send(message)
            print 'sfi: sent'
            response = self.sock.recv(len(message) + 5)
            print 'sfi: recived'
            response_parts = response.split('|')
            print 'sfi: split'
            flag = response_parts[0]; response_parts.remove(flag)
            print 'sfi: flag'
            if flag == 'ACK' and response_parts == message.split('|'):
                # Second step - send file
                file_send(self.sock, data)
                print 'sfi: sent file'
                final_response = self.sock.recv(len(message) + 5)
                print 'sfi: final response'
                self.disconnect()
                print 'sfi: disconnected'
                final_response_parts = final_response.split('|')
                print 'sfi: final parts'
                final_flag = final_response_parts[0]; final_response_parts.remove(final_flag)
                print 'sfi: final flag'
                if final_response_parts == message.split('|'):
                    return final_flag
                else:
                    raise
            else:
                raise
        except Exception, error:
            print 'ERROR', error
            try:
                self.disconnect()
            except Exception, error:
                print 'ERROR', error
                pass # If it didn't manage do disconnect, then it was already closed.
            return 'WTF'
        
    def get_files(self, folder_type, file_list):
        ''' Sends a request for a list of files to the memory module.
        '''
        try:
            # Preperations
            self.connect('memory')
            print 'gfs: connected'
            files = file_list[0]; file_list.remove(files) # There's at least one file
            print 'gfs: 1st'
            for file_name in file_list: # If there's more than one file...
                files+='|{}'.format(file_name)
                print 'gfs: added'
            message = 'FLS|{}|{}'.format(self.username, folder_type)
            # Connection set-up
            self.sock.send(message)
            print 'gfs: sent message'
            response = self.sock.recv(len(message) + 5)
            print 'gfs: got response'
            response_parts = response.split('|')
            flag = response_parts[0]; response_parts.remove(flag)
            if flag == 'ACK' and response_parts == message.split('|'):
                # Files transfer
                print 'gfs: show time!'
                file_send(self.sock, files)
                print 'gfs: sent files'
                data = file_recv(self.sock)
                print 'gfs: recived'
                self.disconnect()
                return 'SCS', data
        except Exception, error:
            print 'ERROR', error
            return 'WTF', 'WTF'
        
    def update_folder(self, folder_type, data):
        ''' Sends a request to update the content of a specific folder to the memory module.
        '''
        try:
            # Connection set-up
            self.connect('memory')
            print 'upd: connected'
            message = 'WRT|{}|{}'.format(self.username, folder_type)
            print 'upd: message made'
            self.sock.send(message)
            print 'upd: sent message'
            response = self.sock.recv(len(message) + 5)
            print 'upd: recived resp'
            response_parts = response.split('|')
            print 'upd: split'
            flag = response_parts[0]; response_parts.remove(flag)
            print 'upd: flag: ' + flag
            if flag == 'ACK' and response_parts == message.split('|'):
                # File send
                file_send(self.sock, data)
                print 'upd: sent file'
                final_response = self.sock.recv(len(message) + 5)
                print 'upd: final recived'
                self.disconnect()
                print 'upd: disconnected'
                final_response_parts = final_response.split('|')
                print 'upd: final split'
                flag = final_response_parts[0]; final_response_parts.remove(flag)
                print 'upd: final flag'
                if final_response_parts == message.split('|'):
                    return flag
                else:
                    raise # Shouldn't get here...
            else:
                raise
        except Exception, error:
            print 'ERROR', error
            self.disconnect()
            return 'WTF'

    def delete_file(self, folder_type, file_name):
        ''' Sends a request to delete a specific file to the memory module.
        '''
        try:
            self.connect('memory')
            print 'del: connected'
            message = 'DEL|{}|{}|{}'.format(self.username, folder_type, file_name)
            print 'del: message made'
            self.sock.send(message)
            print 'del: sent'
            response = self.sock.recv(len(message) + 5)
            print 'del: recived'
            self.disconnect()
            print 'del: disconnected'
            response_parts = response.split('|')
            print 'del: split'
            flag = response_parts[0]; response_parts.remove(flag)
            print 'del: flag'
            if response_parts == message.split('|'):
                return flag
            else:
                raise
        except Exception, error:
            print 'ERROR', error
            return 'WTF'

'''
Exciting. Satisfying. Period.
.
'''
