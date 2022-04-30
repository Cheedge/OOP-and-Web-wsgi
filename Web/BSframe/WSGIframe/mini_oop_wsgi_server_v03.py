"""
mini WSGI Server
version: 0.3 (with wsgi_app_frame_v03.py)
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
    1. set_response_head func
        + recv status and headers from App Frame
        + return self.status and self.headers
        + use environ dict instead pass in func name
            to App Frame.

DONE:
    1. OOP
    2. saperate dynamic request:
        + recv 'status' and 'environ' from
            App Frame then 'set_response_head'
        + if dynamic, recv 'request_body' from
            App Frame

Browser <=> WSGI_Web_Server <=WSGI=> Frame 
"""
import socket
import multiprocessing
import re
import os
import wsgi_app_frame_v03

class WSGI_SERVER(object):
    def __init__(self, PORT) -> None:
        # build server socket
        self.server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # port reuse
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind port
        self.server_sock.bind(("", PORT))
        # listen changed to passive socket
        self.server_sock.listen(128)

    def request_handler(self, servant):
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
        
        # set home page, if 
        if request_src_path == '/':# root
            request_src_path = '/home.html'

        # static request
        if not request_src_path.endswith('.py'):
            try:
                f = open('./templates'+request_src_path, 'rb')
            except Exception as e:
                # request error
                print(f'no such file exist! {request_src_path=}')
                request_line = "HTTP/1.1 404 NOT FOUND\r\n"
                request_head = ""
                request_body = "-------File not exist--------------"
                response = request_line + request_head + '\r\n' + request_body
                servant.send(response.encode('utf-8'))
            else:
                request_line = "HTTP/1.1 200 OK\r\n"
                request_head = ""
                request_body = f.read()
                f.close()
                response = request_line + request_head + '\r\n'
                response += request_body.decode()
                servant.send(response.encode('utf-8'))
        # dynamic request
        else:
            # recv request body from App Frame
            environ = dict()
            environ['Request_Path'] = request_src_path
            request_body = wsgi_app_frame_v03.application(
                environ, self.set_response_head
                )
            request_line = f"HTTP/1.1 {self.status}\r\n"
            for header in self.headers:
                for h_key, h_val in header.items():
                    request_head = f'{h_key}:{h_val}\r\n'
            response = request_line + request_head + '\r\n' + request_body
            print(response)
            servant.send(response.encode('utf-8'))
        servant.close()

    def set_response_head(self, status, headers):
        """
        get 'status'(environ) from App_Frame, and make
        HEAD, so here should use instance attribute
        NOTICE: here not send back to App_Frame, but directly
        called by above, use instance attr (self.head)
        """
        self.status = status
        # add Server info
        self.headers = [{'server': "mini_oop_wsgi_server: version 0.2"}]
        self.headers += headers
    
    def run_server(self):
        while True:
            # block and wait
            servant, _ = self.server_sock.accept()
            # use multiprocess to dispatch servant
            sub_proc = multiprocessing.Process(
                target=self.request_handler,
                args=(servant,)
            )
            # start subprocess
            sub_proc.start()
            """
            main process servant closed, fd(file descrept) -> 1
            then after subprocess finished fd -> 1-1=0,
            which will trigger close response and 4th wavehand begin 
            """
            servant.close()
        # close listen server
        self.server_sock.close()

def main():
    """
    here use main to create a instance of WSGI_SERVER obj
    then invoke the run_server method
    """
    PORT = 8080
    mini_wsgi_server = WSGI_SERVER(PORT)
    mini_wsgi_server.run_server()

if __name__=='__main__':
    main()




