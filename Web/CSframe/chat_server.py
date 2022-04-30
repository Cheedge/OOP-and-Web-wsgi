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

    server_list = [server_sock]
    client_set = set()
    ready_to_read, _, _ = select.select(server_list, [], [])
    # 1, make acceptor to get client ask get (client_sock, address).
    # 2, recv msg from client
    # 3, broadcast msg to every other client
    while True:
        for server in ready_to_read:
            # print(f'{ready_to_read=}')
            print('SERVER: waitting for accept')
            # get client socket
            client_sock, address = server.accept()
            client_set.add(client_sock)
            msg = 'welcome to server'
            msg = f"{len(msg):<{HEADERSIZE}}"+msg
            client_sock.send(bytes(msg,"utf-8"))
            # client_sock.send(bytes('welcome to server'))
            # recieve msg from certain client
            full_message = recv_msg(client_sock)
            full_message = f"{len(full_message):<{HEADERSIZE}}" + full_message.decode('utf-8')
            # broadcast to all other clients
            if len(full_message)==0:
                client_set.remove(client)
                continue
            print(f'{client_set=}')
            for client in client_set:
                print(f'{full_message=}')
                if client != client_sock:
                    client.send(bytes(full_message,"utf-8"))


chat_server_socket()
