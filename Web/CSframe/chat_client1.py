import socket
# import sys
# sys.path.insert(0, '/home/sharma/Desktop/DeepLearning/code_tips/')
# from Web.chat_server import recv_msg

# Header is the length of message
HEADERSIZE = 10
IP = "127.0.0.1"
PORT = 1234
#------------------------------------------------------------
def recv_msg(client_sock) -> str:
    message = b''
    text = b''
    is_new_msg = True
    while True:
        # print('new_receive')
        msg = client_sock.recv(HEADERSIZE)
        # print(f'{msg=}')
        if is_new_msg:
            msg_len = int(msg.decode('utf-8').strip())
            is_new_msg = False

        message += msg
        # print(f'{len(message)=}, {msg_len=}, {message=}')
        if len(message) - HEADERSIZE == msg_len:
            print('all message has been received.')
            is_new_msg = True
            text += message
            message = b''
            break
        if len(msg) == 0:
            print('connection closed')
            # client_sock.close()
            break

    return text
#------------------------------------------------------------





def chat_client_socket()->None:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # solve address already used error
    client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_sock.connect((IP, PORT))
    # Set connection to non-blocking state, so .recv() call won't block, 
    # just return some exception we'll handle
    # client_sock.setblocking(False)
    wait_for_send = True
    while True:
        if wait_for_send:
            snd_msg = input(f'CLIENT 1: ')
            snd_msg = f'{len(snd_msg):<{HEADERSIZE}}' + snd_msg
            client_sock.send(bytes(snd_msg,"utf-8"))
            wait_for_send = False
        else:
            print('CLIENT 1 waitting here')
            rcv_msg = recv_msg(client_sock)
            print(rcv_msg.decode('utf-8'), f'\n client_1 received\n'.upper())
            wait_for_send = True


    # while True:
    #     new_msg = input(f'please give command: ')
    #     new_msg = f'{len(new_msg):<{HEADERSIZE}}' + new_msg
    #     client_sock.send(bytes(new_msg,"utf-8"))
    #     print('CLIENT 1 waitting here')
    #     full_msg = recv_msg(client_sock)
    #     print(full_msg.decode('utf-8'), f'\n client_1 received\n'.upper())
        # new_msg = 'hello server, I am client 1 and I will send msg now'
        # new_msg = f'{len(new_msg):<{HEADERSIZE}}' + new_msg


        # full_msg = recv_msg(client_sock)
        # print(full_msg.decode('utf-8'), f'\n  client recvd all msg\n'.upper())




chat_client_socket()