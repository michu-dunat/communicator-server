from socket import *
import ast
import threading


USER_COUNTER = 0
USERS = []
LENGTH_MULTIPLIER = 1


def delete_salt_from_password(password):
    first_letter = password[0]
    unicode = ord(first_letter)
    step = (unicode % 5) + 2
    password_without_first_letter = password[1:]
    password_without_salt = ""
    for x in range(0, len(password_without_first_letter)):
        if x % step == 0:
            continue
        else:
            password_without_salt += password_without_first_letter[x]

    return password_without_salt


def thread_function(socket):
    global USER_COUNTER, USERS, LENGTH_MULTIPLIER

    connection_socket, addr = socket.accept()
    while True:
        message_as_bytes = connection_socket.recv(1024 * LENGTH_MULTIPLIER)
        message_as_string = message_as_bytes.decode()
        message_as_json = ast.literal_eval(message_as_string)
        if message_as_json['sen'] == "":
            user = 'user' + str(USER_COUNTER)
            USER_COUNTER += 1

            password = delete_salt_from_password(message_as_json['pas'])

            USERS.append([user, password, connection_socket])

            response = {
                'sen': 'server',
                'pas': '',
                'rec': '',
                'msg': user,
            }
            connection_socket.send(str(response).encode())
        else:
            sender_info = []
            for x in USERS:
                if x[0] == message_as_json['sen']:
                    sender_info = x
            if sender_info:
                if sender_info[1] == delete_salt_from_password(message_as_json['pas']):
                    for y in USERS:
                        if y[0] == message_as_json['rec']:
                            message_without_password = message_as_json
                            message_without_password['pas'] = ""
                            y[2].send(str(message_without_password).encode())


if __name__ == '__main__':
    sockets = []
    for i in range(12000, 12051):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(('127.0.0.1', i))
        server_socket.listen(1)
        sockets.append(server_socket)

    for socket in sockets:
        x = threading.Thread(target=thread_function, args=(socket,))
        x.start()
