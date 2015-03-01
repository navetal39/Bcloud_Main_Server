# Info: #
# ===================================


from User import User, ROOT
import zipfile, zlib, os, sys, socket, select

clients_dict = {}

def file_send(sock, mess):
    ''' This method is for sending large files.
    '''
    size = len(mess)
    sock.send('SIZ;{}'.format(size))
    response = sock.recv(5000)
    if response == 'NAK':
        file_send(sock, mess)
        return
    elif response == 'ACK':
        sock.send(mess)
    else: #Just so there'll be an else...
        pass

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
        pri.close()
        pub.close()
        sfz.close()
        mfz.close()
        return 'SCS'
    except:
        return 'WTF'
        
def new_client(name):
    u = User(name)
    clients_dict[name] = u

def respond_to_clients(to_do_list, write_list):
    new_to_do_list = []
    for pair in to_do_list:
        target, data = pair
        if target in write_list:
            info = data.split(';')
            command = info[0]; info.remove(command)
            name = info[0]; info.remove(name)
            if name not in clients_dict.keys():
                new_client(name)
            user = clients_dict[name]
    
            if command == "MNF":
                status = new_user(name)
                new_data = "NONEWDATA"
            elif command == "LUD":
                status, new_data = user.get_folder_info(info[0])
            elif command == "NUD":
                status = user.set_folder_info(info[0], info[1])
                new_data = "NONEWDATA"
            elif command == "GET":
                status, new_data = user.get_folder('public')
            elif command == "WRT":
                status = user.write_to_file(info[0], info[1], info[2])
                new_data = "NONEWDATA"
            elif command == "FIL":
                status, new_data = user.get_file(info[0], info[1])
            else:
                status = "WTF"
                new_data = "NONEWDATA"

            if new_data != 'NONEWDATA':
                if command in ("FIL", "GET"):
                    file_send(target, new_data)
                else:
                    target.send('{};{};{}'.format(status, data, new_data))
            else:
                target.send(status)
            print "Sent data to client" # -For The Record-
        else:
            new_to_do_list.append(pair)
    return new_to_do_list


def main():
    to_do_list = []
    open_sockets = []
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 3330))
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
                if data == "":
                    open_sockets.remove(open_socket)
                    print "Client disconnected"  # -For The Record-
                else:
                    to_do_list.append((open_socket, data))

        to_do_list = respond_to_clients(to_do_list, write_list)


'''
Exciting. Satisfying. Period.
.
'''
