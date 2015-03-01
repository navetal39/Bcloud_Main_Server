# INFO: #
# ===================================

from Database_Management import DataBase
import socket, select, sys
sys.path.append('../')
from COM import *


def respond_to_clients(to_do_list, write_list):
    new_to_do_list = []
    for pair in to_do_list:
        target, data = pair
        if target in write_list:
            info = data.split(';')
            flag = info[0] # flag=command
            info.remove(flag)
            
            if flag == "REG":
                status = database.register_new_user(info[0], info[1])
                
            elif flag == "AUT":
                status = database.authenticate(info[0], info[1])
                
            elif flag == "EXI":
                status = database.name_exists(info[0])
                    
            target.send('{};{}'.format(status, data))
            print "Sent data to client" # -For The Record-
        else:
            new_to_do_list.append(pair)
    return new_to_do_list

def main():
    open_sockets = []
    database=DataBase(MEMORY_IP, MEMORY_PORT)
    to_do_list = []
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 6853))
    server_socket.listen(64)

    while True:
        read_list, write_list, exception_list = select.select([server_socket]+open_sockets, open_sockets, [])
        for open_socket in read_list:
            if open_socket is server_socket:
                new_client_socket, client_addr = open_socket.accept()
                open_sockets.append(new_client_socket)
                print "Client accepted"  # -For The Record-
            else:
                data = open_socket.recv(1024)
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
