# INFO: #
# ===================================

print 'database'

from Database_Management import DataBase
import socket, select, sys
sys.path.append('../')
from COM import *


def respond_to_clients(to_do_list, write_list):
    new_to_do_list = []
    for pair in to_do_list:
        target, data = pair
        print 'data: '+data
        if target in write_list: # If the target is ready to recive a response...
            info = data.split('|')
            flag = info[0] # flag = command
            info.remove(flag)
            
            if flag == "REG":
                print 'registering'
                status = database.register_new_user(info[0], info[1])
                print 'registered'
                
            elif flag == "AUT":
                print 'authenticating'
                status = database.authenticate(info[0], info[1])
                print 'authenticated'
                
            elif flag == "EXI":
                print 'verifying'
                status = database.name_exists(info[0])
                print 'verified'
            
            else:
                print 'unknown command!'
                status = 'WTF'
                print "returning 'WTF'"
            
            our_response = '{}|{}'.format(status, data)
            print 'sending '+ our_response          
            target.send(our_response)
            print "Sent data to client" # -For The Record-
        else: # Target isn't ready, sending it the response will be pointless.
            print 'not in list'
            new_to_do_list.append(pair) # Putting the pair back in the list , to re-visit later.
    return new_to_do_list

def run():
    open_sockets = []
    global database
    database=DataBase(MEMORY_IP, MEMORY_PORT)
    to_do_list = []
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', DATABASE_PORT))
    print "Running... on port {}".format(DATABASE_PORT) # -For The Record-
    server_socket.listen(64)

    while True:
        read_list, write_list, exception_list = select.select([server_socket]+open_sockets, open_sockets, [])
        for open_socket in read_list:
            if open_socket is server_socket: # The main server socket recived a message - It's a new client!
                new_client_socket, client_addr = open_socket.accept()
                open_sockets.append(new_client_socket) # Add to the listening list
                print "Client accepted"  # -For The Record-
            else: # An existing client has sent a message - It's a request!
                data = open_socket.recv(2048)
                if data == '':
                    open_sockets.remove(open_socket)
                    print "Client disconnected"  # -For The Record-
                else:
                    to_do_list.append((open_socket, data))

        to_do_list = respond_to_clients(to_do_list, write_list)


'''
Exciting. Satisfying. Period.
.
'''
