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
            seure_send(sock, 'NAK')
            final_response = file_recv(sock, count+1)
        else:
            final_response = 'WTF'
    else:
        seure_send(sock, 'ACK')
        final_response = sock.recv(size)
    finally:
        return final_response

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

'''
Exciting. Satisfying. Period.
.
'''
