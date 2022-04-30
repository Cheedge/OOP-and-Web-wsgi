import socket
import _thread
import time

"""
_thread.start_new_thread:
1, dispatch a new thread to copy

TODO
1, continue communication with client
2, client 1 <-> server <-> client 2
"""


# global variables
IP = '127.0.0.1'
PORT = 1234


def client_handle(connect) -> None:
    while True:
        rcv_msg = connect.recv(1024)
        bck_msg = b'SERVER>> ' + rcv_msg
        if rcv_msg:
            time.sleep(5)
            connect.send(bck_msg)
        else:
            break
    connect.close()




def server_thread()->None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))
    server.listen(5)

    while True:
        connect, address = server.accept()
        print(f'accept {connect=}, and {address=}')
        _thread.start_new_thread(client_handle, (connect,))


server_thread()