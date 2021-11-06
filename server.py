from socket import *
import ast


def delete_salt_from_password(password):
    first_letter = password[0]
    unicode = ord(first_letter)
    buforek = (unicode % 5) + 2
    password_without_first_letter = password[1:]
    password_without_salt = ""
    for x in range(0, len(password_without_first_letter)):
        if x % buforek == 0:
            continue
        else:
            password_without_salt += password_without_first_letter[x]

    return password_without_salt


if __name__ == '__main__':
    sockets = []
    user_counter = 0
    users = []
    length_multiplier = 1
    for i in range(12000, 12051):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(('127.0.0.1', i))
        server_socket.listen(1)
        sockets.append(server_socket)

    while True:
        for socket in sockets:
            print(socket)
            connection_socket, addr = socket.accept()
            message_as_bytes = connection_socket.recv(1024 * length_multiplier)
            message_as_string = message_as_bytes.decode()
            message_as_json = ast.literal_eval(message_as_string)
            print(message_as_bytes, message_as_string, message_as_json)
            if message_as_json['sen'] == "":
                user = 'user' + str(user_counter)
                user_counter += 1

                password = delete_salt_from_password(message_as_json['pas'])

                users.append([user, password, connection_socket])

                response = {
                    'sen': 'server',
                    'pas': '',
                    'rec': '',
                    'msg': user,
                }
                connection_socket.send(str(response).encode())
            else:
                print('0')
                sender_info = []
                for x in users:
                    print('1')
                    if x[0] == message_as_json['sen']:
                        print('2')
                        sender_info = x
                if sender_info:
                    print('3')
                    if sender_info[1] == delete_salt_from_password(message_as_json['pas']):
                        print('4')
                        for y in users:
                            if y[0] == message_as_json['rec']:
                                print('5')
                                y[2].send(message_as_bytes)
