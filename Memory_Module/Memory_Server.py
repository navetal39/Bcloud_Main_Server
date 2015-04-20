# Info: #
# ===================================


print 'memory'

from User import User, ROOT
import zipfile, zlib, os, sys, socket, Queue
from threading import Thread
sys.path.append('../')
from COM import *
from RECURRING_FUNCTIONS import file_send, file_recv


# Constants: #
## General: ##
NUM_OF_THREADS = 20
SIZE_OF_QUEUE = 40



def new_user(name): # Adds folders and files for a specific user.
    try:
        dirpath = '{r}/{n}'.format(r = ROOT, n = name) # The path for the main folder of the user.
        # Creating the folders:
        os.makedirs(dirpath)
        os.makedirs(dirpath+'/private')
        os.makedirs(dirpath+'/public')
        # Creating the .txt files:
        pri = open (dirpath+'/private.txt', 'w')
        pub = open (dirpath+'/public.txt', 'w')
        # Creating the .zip files:
        flz = zipfile.ZipFile(dirpath+'/files.zip', 'w', compression=zipfile.ZIP_DEFLATED)
        wfz = zipfile.ZipFile(dirpath+'/folder.zip', 'w', compression=zipfile.ZIP_DEFLATED)
        upd = zipfile.ZipFile(dirpath+'/updated_files.zip', 'w', compression=zipfile.ZIP_DEFLATED)
        # Closing the files that were opened:
        pri.close()
        pub.close()
        flz.close()
        wfz.close()
        upd.close()
        return 'SCS'
    except Exception, error: # Somehow an error occured
        print 'ERROR', error
        return 'WTF'

def respond_to_clients(target, data):
    try: # Get the response
        info = data.split('|')
        command = info[0]; info.remove(command)
        name = info[0]; info.remove(name)
        user = User(name)
        
        if command == "MNF": # A request to set-up the user's files and folders
            status = new_user(name)
            print 'made stuff for', name
            new_data = "NONEWDATA"
        elif command == "LUD": # A request for the last updates of a folder's content
            status, new_data = user.get_folder_info(info[0])
            print 'got last update'
        elif command == "NUD": # A request to update the last updates file of a specific folder
            target.send('ACK|{}'.format(data))
            print 'ready for data'
            new_info = file_recv(target) # The content of a file is recived as a file, seperately from the request
            print 'got data'
            status = user.set_folder_info(info[0], new_info)
            print 'set info'
            new_data = "NONEWDATA"
        elif command == "GET": # A request for a complete copy of a folder
            status, new_data = user.get_folder('public') # We don't give away private stuff at all.
            print 'got folder'
        elif command == "WRT": # A request to update a folder's content 
            folder_type = info[0]
            target.send('ACK|{}'.format(data))
            print 'ready for data'
            updated_files = file_recv(target)
            print 'got data'
            status = user.update_folder(folder_type, updated_files)
            print 'updated info'
            new_data = "NONEWDATA"
        elif command == "FLS": # A request to get a list of files
            folder_type = info[0]; info.remove(folder_type)
            print 'ready to get list'
            target.send('ACK|{}'.format(data))
            print 'he now knows it'
            files_list = file_recv(target).split('|') # The list of files can be long, se we transfer it seperately as a file
            print 'got list: ' + str(files_list)
            status, new_data = user.get_files(folder_type, files_list)
            print 'got files'
        elif command == "DEL": # A request to delete a file
            status = user.delete_file(info[0], info[1])
            print 'deleted file'
            new_data = "NONEWDATA"
        else: # An unknown request
            raise
    except Exception, error: # An error occured mid-response-getting
        print 'ERROR', error
        status = "WTF"
        new_data = "NONEWDATA"
    finally: # Sending the response, or the error notification, back to the client.
        if new_data != 'NONEWDATA':
            if command in ("FLS", "GET", "LUD"): # Commands that get a file
                file_send(target, new_data)
            else:
                target.send('{}|{}|{}'.format(status, data, new_data)) # Commands that returns a response, other than a status, that isn't a file.
                                                                       # There are no such commands yet, but these lines are here for future development, if there'll be such a thing.
        else:
            target.send('{}|{}'.format(status, data)) # Commands that only return a status line
        print "Sent data to client"

def do_work():
    while True:
        print 'start'
        client_socket, client_addr = q.get()
        print 'Got a new client!'
        while True:
            try:
                req = client_socket.recv(2048)
            except Exception, e:
                if e.errno == 10054: # A forced connection close
                    req = ''
                else:
                    raise
            print 'req: '+req
            if req == "":
                client_socket.close()
                print "Closed connection" # -For The Record-
                q.task_done()
                break
            else:
                respond_to_clients(client_socket, req)

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
    server_socket.bind(('0.0.0.0',MEMORY_PORT))
    print "Running... on port {}".format(MEMORY_PORT) # -For The Record-
    server_socket.listen(6)

    while True:
        client_socket, client_addr = server_socket.accept()
        print "A client accepted" # -For The Record-
        q.put((client_socket, client_addr))
        print "added to queue"
        if q.full():
            print 'queue is full!'


'''
Exciting. Satisfying. Period.
.
'''
