# INFO: #
# Not tested.
# ===================================

print 'com'

import socket, Queue, sys
from threading import Thread
sys.path.append('../')
from COM import *
from RECURRING_FUNCTIONS import file_send, file_recv

# Constants: #
## General: ##
NUM_OF_THREADS = 20
SIZE_OF_QUEUE = 40
## FLAGS: ##
TO_DATABASE = ("REG", "AUT", "EXI") # List of commands that the database module takes care of that this module may recive.
TO_MEMORY = ("LUD", "GET") # List of commands that the memory module takes care of that this module may recive.

# Methods: #   
## General Methods: ##

def verify(data): # Verifies a user's existance - used before asking the memory module for a folder
    cmd, name, typ = data
    print 'cmd: {}, name: {}, type: {}'.format(cmd, name, typ)
    forward_socket = socket.socket()
    forward_socket.connect((DATABASE_IP, DATABASE_PORT))
    print 'connected to database'
    message = 'EXI|' + name
    print 'sending', message
    forward_socket.send(message)
    response = forward_socket.recv(len(message) + 5)
    print 'recivec', response
    forward_socket.close()
    response_parts = response.split('|')
    print 'splitted'
    flag = response_parts[0]; response_parts.remove(flag)
    print 'flag:', flag
    if response_parts == message.split('|'):
        return flag
    else:
        print 'not matching'
        return 'WTF'

def do_work():
    while True:
        client_socket, client_addr = q.get()
        while True:
            try:
                req = client_socket.recv(2048)
            except Exception, e:
                if e.errno == 10054: # A forced connection close
                    req = ''
                else:
                    raise
            print 'req:', req
            if req == "":
                client_socket.close()
                print "Closed connection" # -For The Record-
                q.task_done()
                break
            else:
                try:
                    data = req.split('|')
                    cmd = data[0]
                    if cmd == 'LUD': # first step - verification
                        db_response = verify(data)
                        print 'database said', db_response
                        if db_response == 'SCS':
                            do = True # All good
                        elif db_response == 'NNM':
                            do = False # Not good
                        else:
                            do = False # Really not good
                    else:
                        do = True # Normal
                    if cmd in TO_MEMORY: # A request for the memory module
                        target_ip = MEMORY_IP
                        target_port = MEMORY_PORT
                        print 'to memory'
                    elif cmd in TO_DATABASE: # A request for the memory module
                        target_ip = DATABASE_IP
                        target_port = DATABASE_PORT
                        print 'to database'
                    else: # An unknown request
                        raise
                except: # An unknown request
                    client_socket.send('WTF')
                else: # A known reques
                    if do: # All was good
                        forward_socket = socket.socket()
                        forward_socket.connect((target_ip, target_port))
                        forward_socket.send(req)
                        if cmd in ('LUD', 'GET'): # The command requests a file
                            module_response = file_recv(forward_socket)
                            file_send(client_socket, module_response)
                        else: # The command requests a simple status response
                            module_response = forward_socket.recv(len(req)+5)
                            client_socket.send(module_response)
                        forward_socket.close()
                    else: # Database said no
                        file_send(client_socket, db_response) # Client expects a file, so we give him a "file"
            

def make_threads_and_queue(num, size):
    global q
    q = Queue.Queue(size)
    for i in xrange(num):
        t = Thread(target=do_work)
        t.deamon = True
        t.start()


## Main Activity Method: ##
def run():
    make_threads_and_queue(NUM_OF_THREADS, SIZE_OF_QUEUE)
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0',HTTP_FRONT_PORT))
    print "Running... on port {}".format(HTTP_FRONT_PORT) # -For The Record-
    server_socket.listen(6)

    while True:
        client_socket, client_addr = server_socket.accept()
        print "A client accepted" # -For The Record-
        q.put((client_socket, client_addr))

'''
Exciting. Satisfying. Period.
.
'''
