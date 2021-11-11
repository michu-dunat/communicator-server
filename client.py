from socket import *
import sys
import ast
import threading
import json


def listener_thread_function(socket):
    while True:
        message_from_client = socket.recv(1024)
        print('Message from Client: ', message_from_client)


def sender_thread_function(socket, username):
    while True:
        receiver_name = input('Receiver login: ')
        if receiver_name == "":
            break
        message = input('Message: ')
        message_to_client = {
            'sen': username,
            'pas': 'abcdefghijklmnoprstuwxyz',
            'rec': receiver_name,
            'msg': message,
        }
        socket.send(str(json.dumps(message_to_client)).encode())


if __name__ == '__main__':
    server_name = '127.0.0.1'
    server_port = int(sys.argv[1])
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    message_to_server = {
                    'sen': '',
                    'pas': 'abcdefghijklmnoprstuwxyz',
                    'rec': 'server',
                    'msg': '',
                }
    client_socket.send(str(json.dumps(message_to_server)).encode())
    reply_from_server = client_socket.recv(1024)
    print('Message from Server: ', reply_from_server)

    username = ast.literal_eval(reply_from_server.decode())['msg']

    x = threading.Thread(target=listener_thread_function, args=(client_socket,))
    x.start()
    y = threading.Thread(target=sender_thread_function, args=(client_socket, username,))
    y.start()

    #clientSocket.close()
