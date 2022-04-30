import socket
import time
import json

HEADERSIZE = 10

def my_server() -> None:
    # build socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind (address, port)
    s.bind((socket.gethostname(), 1234))
    # listen (limit to 5 ps)
    s.listen(5)

    # accept msg
    while True:
        # accept() return (conn, address):
        #   conn is a new socket object usable to send and receive data on the connection
        #   address is the address bound to the socket on the other end of the connection.
        print('new acceptor begin')
        client_socket, address = s.accept()
        print(f'{address= } begin to send message to client')
        # msg = f'this is the message from server service'
        # msg = f'{len(msg):<{HEADERSIZE}}' + msg
        # client_socket.send(bytes(msg, 'utf-8'))
        while True:
            time.sleep(3)
            start = time.time()
            msg_dict = {'name': 'John', 'score': 100, 'time': start, 'favourate': ['apple', 'banana']}
            msg = json.dumps(msg_dict)
            # msg = f'this is the message from server service at {time.time()=}'
            msg = f'{len(msg):<{HEADERSIZE}}' + msg
            client_socket.send(bytes(msg, 'utf-8'))
            print(f'{time.time()-start}')


my_server()




# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((socket.gethostname(), 1243))
# s.listen(5)

# while True:
#     # now our endpoint knows about the OTHER endpoint.
#     clientsocket, address = s.accept()
#     print(f"Connection from {address} has been established.")

#     msg = "Welcome to the server!"
#     msg = f"{len(msg):<{HEADERSIZE}}"+msg

#     clientsocket.send(bytes(msg,"utf-8"))

#     while True:
#         time.sleep(3)
#         msg = f"The time is {time.time()}"
#         msg = f"{len(msg):<{HEADERSIZE}}"+msg

#         print(msg)

#         clientsocket.send(bytes(msg,"utf-8"))
