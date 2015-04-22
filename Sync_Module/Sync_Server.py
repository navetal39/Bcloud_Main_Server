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

def update_files(target, folder_type, user, data = '', again = True):
    if again: #So if the server has to try again it won't ask for the data again.
        secure_send(target, 'UPD') # Server is ready for the file transfer.
        data = secure_file_recv(target) # Recives the files data
    status = user.update_folder(folder_type, data)
    if status != 'SCS':
        if again:
            update_files(target, folder_type, user, data, False) # Try to re-do it one more time.

def send_files(target, folder_type, user, to_send, again = True):
    status, data = user.get_files(folder_type, to_send)
    if status == 'SCS':
        secure_send(target, 'SND')
        response = secure_recv(target)
        if response == 'ACK|SND':
            secure_file_send(target, data)
        else:
            raise # Shouldn't get here...
    elif again:
        send_files(target, folder_type, user, to_send, False)# Try to re-do it one more time.
    else:
        secure_send(target, 'SNF') # Informing the user that the server could not update him. Support currently unimplimented at the client side.

def delete_files(target, folder_type, user, to_delete, again = True):
    secure_send(target, 'DEL')
    response = secure_recv(target)
    if response == 'ACK|DEL':
        bad=[]
        for item in to_delete:
            status = user.delete_file(folder_type, item)
            if status != 'SCS':
                bad.append(item)
        if len(bad) and again: # We give each file a second chance to be deleted.
            delete_files(target, folder_type, user, bad, False)# Try to re-do it one more time.
        else:
            return 'SCS'
    else:
        raise # Shouldn't get here...
        

def sync(target, user, info):
    ''' A method that takes care of the entire sync proccess according to BCSP. Uses 3 helping methods.
    '''
    folder_type, to_send_str, needs_to_update, to_delete_str = info.split('|')
    print 'info split'
    # The server recives long strings of pathes seperated with '<>' instead of lists, so it needs to convert the strings into lists
    to_send = to_send_str.split('<>')
    print '<>'
    to_delete = to_delete_str.split('<>')
    print '<><>'
    if needs_to_update == 'UPDATE': # There are files to recive
        print 'updating files'
        update_files(target, folder_type, user)
        print 'updated files'
    if len(to_send[0]): # There are files to send
        print 'sending files'
        send_files(target, folder_type, user, to_send)
        print 'sent files'
    if len(to_delete[0]): # There are files to delete on this side
        print 'deleting files'
        delete_files(target, folder_type, user, to_delete)
        print 'deleted files'

def respond_to_clients(target, user, data):
    try:
        print 'recived '+data
        info = data.split('|')
        print 'info split'
        command = info[0]; info.remove(command)
        print 'seperated command'

        if command == "LUD": # Request for last update
            status, new_data = user.get_folder_info(info[0])
            print 'got last update'
        elif command == "NUD": # Request to update last updates info
            secure_send(target, 'ACK|{}'.format(data))
            print 'ready for new update'
            new_info = secure_file_recv(target)
            print 'got new update'
            status = user.set_folder_info(info[0], new_info)
            print 'set new update'
            new_data = "NONEWDATA"
        elif command == "SYN": # Request to begin synchronization
            secure_send(target, 'ACK|{}'.format(data))
            print 'ready for sync'
            new_info = secure_file_recv(target)
            print 'got new info'
            sync(target, user, new_info)
            print 'sync finished'
            new_data = "NONEWDATA"
        else:
            raise
        
    except Exception, error:
        print 'ERROR', error
        status = "WTF"
        new_data = "NONEWDATA"
        
    finally:
        if command == "LUD":
            secure_file_send(target, new_data)
        elif command == "SYN":
            secure_send(target, 'FIN')
        else:
            secure_send(target, '{}|{}'.format(status, data))
        print "Sent data to client"

def do_work():
    while True:
        client_socket, client_addr = q.get()
        # Connection set-up:
        authentication_info =  secure_recv(client_socket)
        try:
            cmd, username, password = authentication_info.split('|')
            if cmd == 'AUT':
                user = User(username)
                flag = user.authenticate(password)
            else:
                raise # No reason a valid client should try to set-up a connection without authentication.
        except Exception, error:
            print 'ERROR', error
            flag = 'WTF'
        finally:
            secure_send(client_socket, '{}|{}'.format(flag, authentication_info))
    
        # Requests:
        while True:
            req = secure_recv(client_socket)
            if req == "":
                client_socket.close()
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
    server_socket.bind(('0.0.0.0', SYNC_PORT))
    print "Running... on port {}".format(SYNC_PORT) # -For The Record-
    server_socket.listen(6)

    while True:
        client_socket, client_addr = server_socket.accept()
        print "A client accepted" # -For The Record-
        q.put((client_socket, client_addr))


'''
Exciting. Satisfying. Period.
.
'''
