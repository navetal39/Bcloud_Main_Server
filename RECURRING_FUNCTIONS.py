# INFO: #
# ===================================

# File Transfering: #
def file_recv(sock, count = 0):
    ''' This method is for reciving large files.
    '''
    response = sock.recv(5000)
    flag, str_size = response.split(';')
    try:
        if flag != 'SIZ':
            raise
        size = int(str_size)
    except:
        if count < 3: #Just making sure that it won't attemt endlessly
            sock.send('NAK')
            final_response = file_recv(sock, count+1)
        else:
            final_response = 'WTF'
    else:
        sock.send('ACK')
        final_response = sock.recv(size)
    finally:
        return final_response

def file_send(sock, mess):
    ''' This method is for sending large files.
    '''
    size = len(mess)
    size_message = 'SIZ;{}'.format(size)
    sock.send('SIZ;{}'.format(size))
    response = sock.recv(5000)
    response_parts = response.split(';')
    flag = response_parts[0]; response_parts.remove(flag)
    if response_parts == size_message.split(';'):
        if flag == 'NAK':
            file_send(sock, mess)
            return
        elif flag == 'ACK':
            sock.send(mess)
        else: #Just so there'll be an else...
            pass
    else:
        raise # If, somehow, the program manages to get to this line, it means something went so wrong it deserves to crash.

# Secure communication #:

def secure_accept(server_socket):
    ''' This method needs to accept a new client and establish a secure TCP connection with him (over SSL/TLS).
        It will return exacly what the normal accept method returns UNLESS we will need to change it.
    '''
    cs,ca = server_socket.accept()
    return (cs, ca)

def secure_recv(sock, size = 5000):
    ''' This method needs to receive the encrypted message (the ciphertext), decrypt it and return the plaintext.
    '''
    return sock.recv(size)

def secure_send(sock, mess):
    ''' This method needs to get the message (the plaintext), encrypt it and send it (the ciphertext).
    '''
    print "sending {m}".format(m=mess) # -For The Record-
    sock.send(mess)

def secure_close(sock):
    ''' This method needs to...
    '''
    sock.close()



def secure_file_recv(sock, count = 0):
    ''' This method is for reciving large files.
    '''
    response = secure_recv(sock)
    flag, str_size = response.split(';')
    try:
        if flag != 'SIZ':
            raise
        size = int(str_size)
    except:
        if count < 3: #Just making sure that it won't attemt endlessly
            seure_send(sock, 'NAK;'+response)
            final_response = secure_file_recv(sock, count+1)
        else:
            final_response = 'WTF'
    else:
        seure_send(sock, 'ACK;'+response)
        final_response = secure_recv(sock, size)
    finally:
        return final_response

def secure_file_send(sock, mess):
    ''' This method is for sending large files.
    '''
    size = len(mess)
    size_message = 'SIZ;{}'.format(size)
    secure_send(sock, size_message)
    response = sock.recv(5000)
    response_parts = response.split(';')
    flag = response_parts[0]; response_parts.remove(flag)
    if flag == 'NAK':
        secure_file_send(sock, mess)
        return
    elif flag == 'ACK':
        secure_send(sock, mess)
    else: #Just so there'll be an else...
        pass



'''
Exciting. Satisfying. Period.
.
'''
