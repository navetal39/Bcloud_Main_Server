# INFO: #
# First version.
# ===================================

from Database_Management import *
import socket
import select

open_sockets = []

def respond_to_clients(to_do_list, write_list):
    new_to_do_list = []
    for pair in to_do_list:
        target, data = pair
        if target in write_list:
            info = data.split(';')
            flag = parts[0]
            info.remove(flag)
            
            if flag=="REG":
                status = register_new_user(info[0], info[1])
                
            elif flag=="AUT":
                status = authenticate(info[0], info[1])
                
            elif flag=="EXI":
                status = name_exists(info[0])
                    
            open_socket.send(status+';'+data)
            print "Sent data to client" # -For The Record-
        else:
            updated_ml.append(pair)
    return new_to_do_list

#def Main():
    to_do_list = []
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 6853))
    server_socket.listen(6)

    while True:
        read_list, write_list, exception_list = select.select([server_socket]+open_sockets, open_sockets, [])
        for open_socket in read_list:
            if open_socket in server_socket:
                new_client_soclet, client_addr = open_socket.accept()
                open_sockets.append(new_client_socket)
                print "Client accepted"  # -For The Record-
            else:
                data = open_socket.recv(1024)
                if rdata == '':
                    open_sockets.remove(open_socket)
                    print "Client disconnected"  # -For The Record-
                else:
                    to_do_list.append((open_socket, data))

        to_do_list = Respond_To_Clients(to_do_list, write_list)




'''
Exciting. Satisfying. Period.
.
'''
