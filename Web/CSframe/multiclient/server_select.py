from os import readlink
import socket
import time
import select


"""
select
asynchronous

TODO
1, continue communication with client (DONE)
2, client 1 <-> server <-> client 2 (Done)
3, if server crl+c closed, client should also
   closed (Done)
4, when input is '\n', it should recognize(Done)
5, distinguish input ' ' with server close.(same
    as 3)
"""

# global variables
IP = '127.0.0.1'
PORT = 1234

def server_select()-> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))
    server.listen(5)

    # contain server and connections
    sock_list = [server]

    while True:
        # select:   when sock_list has any change(means response or new add)
        #           the select will triger, and pass a new "flow"
        read_list, _, _ = select.select(sock_list, [], sock_list)

        for sock in read_list:
            if sock == server:
                connect, address = sock.accept()
                print(f'server accept {connect=}, and {address=}')
                sock_list.append(connect)

            else:
                msg = sock.recv(1024)
                # print(f'{msg=}')
                # if not remove the "dead" sock, next loop will be destroied.
                # if sock is Crl+c, the msg will be b''.
                if msg:
                    msg = b'SERVER>> ' + msg
                    time.sleep(5)
                    sock.send(msg)
                    # print(sock)
                else:
                    sock.close()
                    sock_list.remove(sock)


server_select()