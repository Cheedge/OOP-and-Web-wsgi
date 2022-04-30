import socket
from os import fork, waitpid, WNOHANG, _exit, kill, getpid
import time

"""
server socket using os.fork:
using fork to construct a new process which
connect to same server and accept same client
to receive msg prallel.

fork:
1, copy
2, clear

TODO:
1, continue communication with client
2, client 1 <-> server <-> client 2
"""

# global params:
PORT = 1234
IP = '127.0.0.1'

def clear_child_zombies(acctive_child) -> None:
    # pid = getpid()
    # print(f'{pid=}')
    # notice here cannot use for loop will still left zombie ps
    while acctive_child:
        
        try:
            child_pid, _ = waitpid(0, WNOHANG)
            if child_pid != 0: # has child process
                print(f'inside the {child_pid=}, {acctive_child=} ')
                acctive_child.remove(child_pid)
                # kill(child_pid, 9)
        except ChildProcessError:
            print(f'no child ps')

def server_fork()->None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # solve address already in used error
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))
    server.listen(5)

    acctive_child=list()
    while True:
        connect, address = server.accept()
        # clean child zombies
        clear_child_zombies(acctive_child)
        # make new fork
        is_child = fork()
        print(f'{is_child=}')
        # if is_child != 0:# it is org connect ps
        if is_child == 0:# it is forked child ps
            msg = connect.recv(1024)
            msg = b'SERVER>> '+msg
            time.sleep(5)
            connect.send(msg)
            connect.close()
            _exit(0)
        else:
            acctive_child.append(is_child)

server_fork()



