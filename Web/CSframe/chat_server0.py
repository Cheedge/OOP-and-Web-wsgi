import socket
import select

# Header is the length of message
HEADERSIZE = 10
IP = "127.0.0.1"
PORT = 1234

def send_msg(client_sock, msg: str) -> None:
    client_sock.send(msg)


def recv_msg(client_sock) -> str:
    message = b''
    text = b''
    is_new_msg = True
    while True:
        msg = client_sock.recv(HEADERSIZE)
        if is_new_msg:
            msg_len = int(msg.decode('utf-8').strip())
            is_new_msg = False

        message += msg
        if len(message) - HEADERSIZE == msg_len:
            print('all message has been received.')
            is_new_msg = True
            text += message
            message = b''
            break
        if msg is None:
            print('connection closed')
            # client_sock.close()
            break

    return text
    # usr = {'header': msg, 'data': client_sock.recv(msg_len)}

def chat_server_socket()-> None:
    # build socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # solve address already used error
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind (IP, Port)
    server_sock.bind((IP, PORT))
    # listen
    server_sock.listen(5)
    
    socket_list = [server_sock]
    # socket_list_before_select = [server_sock]
    # client_set = set()
    # ready_to_read, _, _ = select.select(server_list, [], [])
    # 1, make acceptor to get client ask get (client_sock, address).
    # 2, recv msg from client
    # 3, broadcast msg to every other client
    while True:
        # print('new round')
        # socket_list, _, _ = select.select(socket_list_before_select, [], [])
        # print(f'{socket_list_before_select=}')
        for sock in socket_list:
            
            if sock == server_sock:
                # print(f'{socket_list= }')
                client_sock, _ = sock.accept()
                print('after accept')
                socket_list.append(client_sock)
                # socket_list_before_select.append(client_sock)
                msg = recv_msg(client_sock)
                # print(f'{msg=}')
                msg = f'{len(msg):<{HEADERSIZE}}' + msg.decode('utf-8')
            else:# when sock is client
                for s in socket_list[1:]:
                    if s != server_sock:
                        # print(f'{s=}, {sock=}')
                        s.send(bytes(msg, 'utf-8'))
                        # print(f'{msg=}')
                # socket_list.remove(sock)





    # client_sock, _ = server_sock.accept()
    # # client_set.add(client_sock)
    # welcome_msg = f'welcome to server'
    # welcome_msg = f'{len(welcome_msg):<{HEADERSIZE}}' + welcome_msg
    # client_sock.send(bytes(welcome_msg, 'utf-8'))
    # while True:
    #     for client in client_set:
    #         print('SERVER waitting here')
    #         msg = recv_msg(client)
    #         if msg:
    #             if client != client_sock:
    #                 client.send(msg)
chat_server_socket()