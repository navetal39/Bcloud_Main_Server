# Info: #
# NOT TESTED YET
# ===================================

print 'sync'

from User import User
import zipfile, zlib, sys, os, socket, Queue
sys.path.append('../')
from COM import *
from RECURRING_FUNCTIONS import *
from threading import Thread


# Constants: #
## General: ##
NUM_OF_THREADS = 20
SIZE_OF_QUEUE = 40

def update_files(target, folder_type, user, again = True):
    if again: #So if the server has to try again it won't ask for the data again.
        secure_send(target, 'UPD') # Server is ready for the file transfer.
        data = secure_file_recv(target)
    status = user.update_folder(folder_type, data)
    if status != 'SCS':
        if again:
            update_files(target, folder_type, user, False)

def send_files(target, folder_type, user, to_send, again = True):
    status, data = user.get_files(folder_type, to_send)
    if status == 'SCS':
        secure_send(target, 'SND')
        response = secure_recv(target, 7)
        if response == 'ACK|SND':
            secure_file_send(target, data)
        else:
            raise # Shouldn't get here...
    elif again:
        send_files(target, folder_type, user, to_send, False)
    else:
        secure_send(target, 'SNF')
        secure_file_send(target, 'SNF')

def delete_files(target, folder_type, user, to_delete, again = True):
    secure_send(target, 'DEL')
    response = secure_recv(target, 7)
    if response == 'ACK|DEL':
        bad=[]
        for item in to_delete:
            status = user.delete_file(folder_type, item)
            if status != 'SCS':
                bad.append(item)
        if len(bad) and again: # We give each file a second chance to be deleted.
            delete_files(target, flder_type, user, bad, False)
        else:
            return 'SCS'
    else:
        raise # Shouldn't get here...
        

def sync(target, user, info):
    folder_type, to_send_str, to_update_str, to_delete_str = info.split('|')
    to_send = to_send_str.split('<>')
    to_update = to_update_str.split('<>')
    to_delete = to_delete_str.split('<>')
    if len(to_update[0]): # There are files
        update_files(target, folder_type, user) # There's no need to give the function the list of files that needs to be updated since all the system does it extracting all files. The list exist in case we'll need it in the future.
    if len(to_send[0]): # There are files
        send_files(target, folder_type, user, to_send)
    if len(to_delete[0]): # There are files
        delete_files(target, user, folder_type, to_delete)    

def respond_to_clients(target, user, data):
    try:
        info = data.split('|')
        command = info[0]; info.remove(command)

        if command == "LUD":
            status, new_data = user.get_folder_info(info[0])
        elif command == "NUD":
            secure_send(target, 'ACK|{}'.format(data))
            new_info = secure_file_recv(target)
            status = user.set_folder_info(info[0], new_info)
            new_data = "NONEWDATA"
        elif command == "SYN":
            secure_send(target, 'ACK|{}'.format(data))
            new_info = secure_file_recv(target)
            sync(target, user, new_info)
            new_data = "NONEWDATA"
        else:
            raise
        
    except:
        status = "WTF"
        new_data = "NONEWDATA"
        
    finally:
        if command == "LUD":
            file_send(target, new_data)
        elif command == "SYN":
            secure_send(target, 'FIN')
        else:
            secure_send(target, '{}|{}'.format(status, data))
        print "Sent data to client"

def do_work():
    client_socket, client_addr = q.get()
    # Connection set-up:
    authentication_info =  secure_recv(client_socket)
    try:
        cmd, username, password = authentication_info.split('|')
        if cmd == 'AUT':
            user = User(username)
            flag = user.authenticate(password)
        else:
            raise
    except:
        flag = 'WTF'
    finally:
        secure_send('{}|{}'.format(flag, authentication_info))
    
    # Requests:
    while True:
        req = secure_recv(client_socket)
        if req == "":
            secure_close(client_socket)
            print "Closed connection" # -For The Record-
            q.task_done()
            break
        else:
            respond_to_clients(client_socket, user, req)

def make_threads_and_queue(num, size):
    global q
    q = Queue.Queue(size)
    for i in xrange(num):
        t = Thread(target=do_work)
        t.deamon = True
        t.start()


def run():
    make_threads_and_queue(NUM_OF_THREADS, SIZE_OF_QUEUE)
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0',SYNC_PORT))
    print "Running... on port {}".format(SYNC_PORT) # -For The Record-
    server_socket.listen(6)

    while True:
        client_socket, client_addr = secure_accept(server_socket)
        print "A client accepted" # -For The Record-
        q.put((client_socket, client_addr))


'''
Exciting. Satisfying. Period.
.
'''
