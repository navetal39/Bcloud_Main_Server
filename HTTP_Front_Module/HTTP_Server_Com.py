# INFO: #
# Not tested.
# ===================================

import socket, Queue, sys
from threading import Thread
sys.path.append('../')
from COM import *
from REACURRING_FUNCTIONS import file_send, file_recv

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
                data = req.split(';')
                cmd = data[0]
                get = False
                if cmd == 'GET':
                    cmd == 'EXI'
                    req = 'EXI;{}'.format(data[1]) # Change the command on the request
                    get = True
                if cmd in TO_MEMORY: # A request for the memory module
                    target_ip = MEMORY_IP
                    target_port = MEMORY_PORT
                elif cmd in TO_DATABASE: # A request for the memory module
                    target_ip = DATABASE_IP
                    target_port = DATABASE_PORT
                else: # An unknown request
                    raise
            except: # An unknown request
                client_socket.send('WTF')
            else: # A known reques
                forward_socket = socket.socket()
                forward_socket.connect((target_ip, target_port))
                forward_socket.send(req)
                module_response = forward_socket.recv(5000)
                forward_socket.close()
                if get: # It was a get request, thus it requires a second operation - obtaining the folder
                    parsed_module_response = module_response.split(';')
                    flag = parsed_module_response[0]
                    if flag == 'SCS': # Only if the name exists this flag should appear, and only then we should attemt to get the folder
                        req = 'GET;{}'.format(data[1]) # Return the request to it's original form
                        forward_socket.connect((MEMORY_IP, MEMORY_PORT))
                        forward_socket.send(req)
                        module_response = file_recv(forward_socket)
                        forward_socket.close()
                    elif flag == 'NNM':
                        module_response = 'NNM'
                    else:
                        module_response = 'WTF'
                    file_send(client_socket, module_response)
                else:
                    client_socket.send(module_response)
            

def make_threads_and_queue(num, size):
    global q
    q = Queue.Queue(size)
    for i in xrange(num):
        t = Thread(target=do_work)
        t.deamon = True
        t.start()


## Main Activity Method: ##
def main():
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
