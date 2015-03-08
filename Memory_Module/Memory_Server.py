# Info: #
# ===================================


from User import User, ROOT
import zipfile, zlib, os, sys, socket
sys.path.append('../')
from COM import *
from RECURRING_FUNCTIONS import file_send, file_recv


# Constants: #
## General: ##
NUM_OF_THREADS = 20
SIZE_OF_QUEUE = 40



def new_user(name):
    try:
        dirpath = '{r}/{n}'.format(r = ROOT, n = name)
        os.makedirs(dirpath)
        os.makedirs(dirpath+'/private')
        os.makedirs(dirpath+'/public')
        pri = open (dirpath+'/private.txt', 'w')
        pub = open (dirpath+'/public.txt', 'w')
        sfz = zipfile.ZipFile(dirpath+'/single.zip', 'w', compression=zipfile.ZIP_DEFLATED)
        mfz = zipfile.ZipFile(dirpath+'/folder.zip', 'w', compression=zipfile.ZIP_DEFLATED)
        upd = zipfile.ZipFile(dirpath+'/updated_files.zip', 'w', compression=zipfile.ZIP_DEFLATED)
        pri.close()
        pub.close()
        sfz.close()
        mfz.close()
        upd.close()
        return 'SCS'
    except:
        return 'WTF'

def respond_to_clients(target, data):
    try:
        info = data.split('|')
        command = info[0]; info.remove(command)
        name = info[0]; info.remove(name)
        user = User(name)
        
        if command == "MNF":
            status = new_user(name)
            new_data = "NONEWDATA"
        elif command == "LUD":
            status, new_data = user.get_folder_info(info[0])
        elif command == "NUD":
            target.send('ACK|{}'.format(data))
            new_info = file_recv(target)
            status = user.set_folder_info(info[0], new_info)
            new_data = "NONEWDATA"
        elif command == "GET":
            status, new_data = user.get_folder('public')
        elif command == "WRT":
            target.send('ACK|{}'.format(data))
            updated_files = file_recv(target)
            status = user.update_folder(updated_files)
            new_data = "NONEWDATA"
        elif command == "FIL":
            status, new_data = user.get_file(info[0], info[1])
        elif command == "DEL":
            status = user.delete_file(info[0], info[1])
            new_data = "NONEWDATA"
        else:
            raise
    except:
        status = "WTF"
        new_data = "NONEWDATA"
    finally:
        if new_data != 'NONEWDATA':
            if command in ("FIL", "GET", "LUD"):
                file_send(target, new_data)
            else:
                target.send('{}|{}|{}'.format(status, data, new_data))
        else:
            target.send('{}|[}'.format(status, data))
        print "Sent data to client"

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
            respond_to_clients(client_socket, req)

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
        client_socket, client_addr = server_socket.accept()
        print "A client accepted" # -For The Record-
        q.put((client_socket, client_addr))


'''
Exciting. Satisfying. Period.
.
'''
