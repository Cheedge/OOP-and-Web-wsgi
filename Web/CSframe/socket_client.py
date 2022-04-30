import socket
import json


HEADERSIZE = 10

def my_client()->None:
    # build socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to (address, port)
    s.connect((socket.gethostname(), 1234))

    # recv msg
    # msg = s.recv(8)
    # print(msg.decode('utf-8'))
    # s.close()

    message = b''
    # message = ''
    is_new_message = True
    while True:
        print('new recver begin')
        msg = s.recv(16)

        if is_new_message:
            msg_len = int(msg[:HEADERSIZE])
            is_new_message = False

        message += msg
        # message += msg.decode('utf-8')
        if len(message)-msg_len == HEADERSIZE:
            is_new_message = True
            print(message)
            # Notice: json.loads can only serilize 1 dict,
            # means json.loads({}{}) or json.loads(''{}) is wrong
            # so here remove the header part.
            print(json.loads(message[HEADERSIZE:]))
            message = b''
            # print(f'client has recvd {message= } from server')
            # message = ''



    # print(f'client has recvd {message= } from server')
    s.close()

my_client()




# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostname(), 1243))

# while True:
#     full_msg = ''
#     new_msg = True
#     while True:
#         msg = s.recv(16)
#         if new_msg:
#             print("new msg len:",msg[:HEADERSIZE])
#             msglen = int(msg[:HEADERSIZE])
#             new_msg = False

#         print(f"full message length: {msglen}")

#         full_msg += msg.decode("utf-8")

#         print(len(full_msg))


#         if len(full_msg)-HEADERSIZE == msglen:
#             print("full msg recvd")
#             print(full_msg[HEADERSIZE:])
#             new_msg = True
#             full_msg = ""