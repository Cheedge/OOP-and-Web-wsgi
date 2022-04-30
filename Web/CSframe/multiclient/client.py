from posix import ST_RELATIME
import socket

"""

1, continue communication with client (DONE)
2, client 1 <-> server <-> client 2 (Done)
3, if server crl+c closed, client should also
   closed (Done)
4, when input is '\n', it should recognize(Done)
5, distinguish input ' ' with server close.(same
    as 3)
"""

# globle variable
IP = '127.0.0.1'
PORT = 1234

def client()->None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    while True:
        snd_msg = input(f'your message>> ')
        #here must not be empty str (f''), as None type cannot encode.
        if not snd_msg:
            snd_msg = f' '
        
        client.send(snd_msg.encode())
        rcv_msg = client.recv(1024).decode('utf-8')
        if not rcv_msg:
            client.close()
            break
        else:
            print(f'{rcv_msg=}')

client()
