"""
mini WSGI Server
version: 0
functionality:
    realize basic Web Server functionality
    recv request/ send response with Browser
    realize basic WSGI communication with Frame 
    realize basic render html with css, js

Web Server:
    only used for communication
App Frame:
    prepare and assemble html.
WSGI:
    protocal between Web Server and App Frame.
    + WSGI_Web_Server:
        include a 'set_response_head' func providing
        for App Frame to call
    + WSGI_App_Frame:
        include a 'application(env, set_response_head'
        func to be called by Web Server to get the whole
        html.

TODO:
    1. OOP
    2. saperate dynamic request
    3. set_response_head func

Browser <=> WSGI_Web_Server <=WSGI=> Frame 
"""
import socket
import multiprocessing
import re
import os

def request_handler(servant):
    recv_data = servant.recv(1024)
    print('recv data')
    if len(recv_data) == 0:
        print(f'here use short connection, so after 5min no msg, client closed')
        return
    # decode request data
    # notice here need to = to 
    recv_data = recv_data.decode()
    print('>>'*20,f'\n{recv_data=},{os.getpid()=}')
    # GET / HTTP/1.1
    # this is more easy way
    # path_list = recv_data.split(' ')
    
    """
    IndexError: list index out of range
    the server will send
    msg automaticly(when no operation). Then recv_data=''
    and the path_list[1] will cause error
    """

    request_list = recv_data.splitlines()
    request_src_path = re.match(r'[^/]+(/[^ ]*)', request_list[0]).group(1)
    print('%'*10, f'{request_src_path=}')
    
    # set home page, if 
    if request_src_path == '/':# root
        request_src_path = '/home.html'
    
    
    try:
       f = open('./templates'+request_src_path, 'rb')
    except Exception as e:
        print(f'no such file exist! {request_src_path=}')
        request_line = "HTTP/1.1 404 NOT FOUND\r\n"
        request_head = ""
        request_body = "File not exist"
        response = request_line + request_head + '\r\n' + request_body
        servant.send(response.encode())
    else:
        request_line = "HTTP/1.1 200 OK\r\n"
        request_head = ""
        request_body = f.read()
        response = request_line + request_head + '\r\n'
        # response.encode()
        response += request_body.decode()
        servant.send(response.encode())
        # print('!!!'*3, f'before handler servant close {os.getpid()=}')

    servant.close()
    # print('!!!'*3, f'after handler servant close {os.getpid()=}')


IP = "127.0.0.1"
PORT = 8080
def main():
    # build server socket
    server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # port reuse
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind port
    server_sock.bind((IP, PORT))
    # listen changed to passive socket
    server_sock.listen(128)
    # print('begin while')

    while True:
        # block and wait
        servant, _ = server_sock.accept()
        # print('accept')
        # use multiprocess to dispatch servant
        sub_proc = multiprocessing.Process(
            target=request_handler,
            args=(servant,)
        )
        # start subprocess
        sub_proc.start()
        # print('???'*3, f'beore main servant close {os.getpid()=}')
        """
        main process servant closed, fd(file descrept) -> 1
        then after subprocess finished fd -> 1-1=0,
        which will trigger close response and 4th wavehand begin 
        """
        # request_handler(servant)
        servant.close()
        # print('???'*3, f'after main servant close {os.getpid()=}')

    # close listen server
    server_sock.close()

if __name__=='__main__':
    print('run server')
    main()



