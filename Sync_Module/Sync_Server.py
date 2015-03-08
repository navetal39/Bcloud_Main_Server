# Info: #
# ===================================


from User import User
import zipfile, zlib, sys, os, socket
sys.path.append('../')
from COM import *
from RECURRING_FUNCTIONS import *


# Constants: #
## General: ##
NUM_OF_THREADS = 20
SIZE_OF_QUEUE = 40

def update_files(target, user, to_update):
    pass

def send_files(target, user, to_send):
    pass

def delete_files(target, user, to_delete):
    for path in to_delete:
        

def sync(target, user, info):
    to_send, to_update, to_delete = info
    update_status = update_files(target, user, to_update)
    send_status = send_files(target, user, to_send)
    delete_status = delete_files(target, user, to_delete)

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
            status = sync(target, user, info)
        else:
            raise
    except:
        status = "WTF"
        new_data = "NONEWDATA"
    finally:
        if new_data != 'NONEWDATA':
            if command in ("LUD", ""):
                file_send(target, new_data)
            else:
                target.send('{}|{}|{}'.format(status, data, new_data))
        else:
            target.send('{}|[}'.format(status, data))
        print "Sent data to client"

def do_work():
    client_socket, client_addr = q.get()
    # Connection set-up:
    authentication_info =  secure_recv(client_socket)
    try:
        flag, username, password = authentication_info.split('|')
        user = User(username)
        flag = user.authenticate(password)
    except:
        flag = 'WTF'
    finally:
        secure_send('{}|{}'.format(flag, authentication_info)

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


def main():
    make_threads_and_queue(NUM_OF_THREADS, SIZE_OF_QUEUE)
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0',HTTP_FRONT_PORT))
    print "Running... on port {}".format(HTTP_FRONT_PORT) # -For The Record-
    server_socket.listen(6)

    while True:
        client_socket, client_addr = secure_accept(server_socket)
        print "A client accepted" # -For The Record-
        q.put((client_socket, client_addr))


'''
Exciting. Satisfying. Period.
.
'''
