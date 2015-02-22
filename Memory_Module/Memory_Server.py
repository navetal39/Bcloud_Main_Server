# Info: #
# Pre-first version
# ===================================

'''
To do:
1) Add the part that adds new folders.
2) Add the part that makes new User objects.
'''
from classes import User, ROOT
import zipfile, os, sys

clients_dict = {}

def new_user(name):
    try:
        dirpath='{r}/{n}'.format(r = ROOT, n = name)
        os.makedirs(dirpath)
        os.makedirs(dirpath+'/private')
        os.makedirs(dirpath+'/public')
        pri = open (dirpath+'/private.txt', 'w')
        pub = open (dirpath+'/public.txt', 'w')
        sfz = zipfile.ZipFile(dirpath+'/single.zip', 'w')
        mfz = zipfile.ZipFile(dirpath+'/folder.zip', 'w')
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
            flag = info[0] # flag=command
            info.remove(flag)
            name=parts[0]
            info.remove(name)
            user=clients_dict[name]
            if flag == "MNF":
                status = new_user(name)
                new_data = 'MNFREQNEWDATAPLACEHOLDERABCDEFGHIJKLMNOPQRSTUVWXYZBCLOUDISCOOL'
            elif flag == "LUD":
                status, new_data = user.get_folder_info(info[0])
                
            elif flag == "GET":
                status, new_data = user.get_folder(info[0])

            elif flag == "FIL":
                status, new_data = user.get_file(info[0], info[1])

            if newdata != 'MNFREQNEWDATAPLACEHOLDERABCDEFGHIJKLMNOPQRSTUVWXYZBCLOUDISCOOL'
                target.send(status+';'+new_data)
            else:
                target.send(status)
            print "Sent data to client" # -For The Record-
        else:
            new_to_do_list.append(pair)
    return new_to_do_list


def Main():
    to_do_list = []
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 3330))
    server_socket.listen(6)

    while True:
        read_list, write_list, exception_list = select.select([server_socket]+open_sockets, open_sockets, [])
        for open_socket in read_list:
            if open_socket is server_socket:
                new_client_socket, client_addr = open_socket.accept()
                open_sockets.append(new_client_socket)
                print "Client accepted"  # -For The Record-
            else:
                data = open_socket.recv(1024)
                if data == '':
                    open_sockets.remove(open_socket)
                    print "Client disconnected"  # -For The Record-
                else:
                    to_do_list.append((open_socket, data))

        to_do_list = Respond_To_Clients(to_do_list, write_list)


'''
Exciting. Satisfying. Period.
.
'''
