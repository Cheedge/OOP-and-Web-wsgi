"""
mini WSGI Server
version: 02
functionality:
    realize basic Web Server functionality
    recv request/ send response with Browser
    realize basic WSGI communication with Frame 
    realize basic render html with css, js

Browser <=> Web_Server <=WSGI=> Frame 

new:
    + use gevent
"""
import socket
import gevent
from gevent import monkey

monkey.patch_all()

def request_handler(servant):
    recv_data = servant.recv(100000)
    print('recv data')
    if len(recv_data) == 0:
        print(f'here use short connection, so after 5min no msg, client closed')
        return
    # decode request data
    # notice here need to = to 
    recv_data = recv_data.decode()
    # GET / HTTP/1.1
    path_list = recv_data.split(' ')
    
    request_src_path = path_list[1]
    # set home page
    if path_list == '/':# root
        request_src_path = '/home.html'
    
    
    try:
       f = open('./html'+request_src_path, 'rb')
    except Exception as e:
        print(f'no such file exist!')
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
        response.encode() 
        response += request_body
        servant.send(response)

    servant.close()


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
    print('begin while')

    while True:
        # block and wait
        servant, _ = server_sock.accept()
        print('accept')
        # use multiprocess to dispatch servant
        gevent.spawn(request_handler, servant)

        # start subprocess
        # thrd.start()

        """
        main process servant closed, fd(file descrept) -> 1
        then after subprocess finished fd -> 1-1=0,
        which will trigger close response and 4th wavehand begin 
        """
        # servant.close()

    # close listen server
    server_sock.close()

if __name__=='__main__':
    print('run server')
    main()



