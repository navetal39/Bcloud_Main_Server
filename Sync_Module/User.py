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
            print 'aut: connected'
            message = 'AUT|{}|{}'.format(self.username, password)
            print 'aut: made message'
            self.sock.send(message)
            print 'aut: sent'
            response = self.sock.recv(5000)
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
        try:
            self.connect('memory')
            print 'sfi: connceted'
            message = 'NUD|{}|{}'.format(self.username, folder_type)
            print 'sfi: made message'
            self.sock.send(message)
            print 'sfi: sent'
            response = self.sock.recv(5000)
            print 'sfi: recived'
            response_parts = response.split('|')
            print 'sfi: split'
            flag = response_parts[0]; response_parts.remove(flag)
            print 'sfi: flag'
            if flag == 'ACK' and response_parts == message.split('|'):
                file_send(self.sock, data)
                print 'sfi: sent file'
                final_response = self.sock.recv(5000)
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
        try:
            self.connect('memory')
            print 'gfs: connected'
            files = file_list[0]; file_list.remove(files) # There's at least one file
            print 'gfs: 1st'
            for file_name in file_list: # If there's more than one file
                files+='|{}'.format(file_name)
                print 'gfs: added'
            self.sock.send('FLS|{}|{}|{}'.format(self.username, folder_type, files))
            print 'gfs: made message'
            data = file_recv(self.sock)
            print 'gfs: recived'
            self.disconnect()
            return 'SCS', data
        except Exception, error:
            print 'ERROR', error
            return 'WTF', 'WTF'
        
    def update_folder(self, folder_type, data):
        try:
            self.connect('memory')
            print 'upd: connected'
            message = 'WRT|{}|{}'.format(self.username, folder_type)
            print 'upd: message made'
            self.sock.send(message)
            print 'upd: sent message'
            response = self.sock.recv(5000)
            print 'upd: recived resp'
            response_parts = response.split('|')
            print 'upd: split'
            flag = response_parts[0]; response_parts.remove(flag)
            print 'upd: flag: ' + flag
            if flag == 'ACK' and response_parts == message.split('|'):
                file_send(self.sock, data)
                print 'upd: sent file'
                final_response = self.sock.recv(5000)
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
        try:
            self.connect('memory')
            print 'del: connected'
            message = 'DEL|{}|{}|{}'.format(self.username, folder_type, file_name)
            print 'del: message made'
            self.sock.send(message)
            print 'del: sent'
            response = self.sock.recv(5000)
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
