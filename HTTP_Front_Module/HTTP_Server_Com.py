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
TO_DATABASE = ("REG", "AUT", "EXI")
TO_MEMORY = ("MNF", "LUD", "GET", "NUD", "WRT", "FIL")

# Methods: #   
## General Methods: ##
def do_work():
    client_socket, client_addr = q.get()
    while True:
        req = client_socket.recv(5000)
        if req == "":
            client_socket.close()
            print "Closed connection" # -For The Record-
            q.task_done()
            break
        else:
            try:
                data = req.split('|')
                cmd = data[0]
                get = False
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
                forward_socket = socket.socket()
                forward_socket.connect((target_ip, target_port))
                forward_socket.send(req)
                if cmd in ('LUD', 'GET'):
                    module_response = file_recv(forward_socket)
                    file_send(client_socket, module_response)
                else:
                    module_response = forward_socket.recv(5000)
                    client_socket.send(module_response)
                forward_socket.close()
            

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
