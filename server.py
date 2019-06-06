#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import threading, time, socket
import database


def now():
    return time.ctime(time.time())

class ChatServer(object):

    def __init__(self, host='localhost', port=6777):
        self.__host=host
        self.__port=port
        self.connections={}
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msgs={
            "start": "Starting server on port {} and host '{}'\n",
            "connect": "{} user '{}'{} connected",
            "user_left": "{} user '{}' left from chat",
            "send_to_all":"{}: {}",
            "send_pm": "pm from {}: {}",
            "welcome":"Welcome to chat server, please enter your nickname: \r\n"
        }
        self.db = database.Database("chat.db")

    def userlist(self):
        return self.connections.keys()

    def close_connection(self, connection):
        self.connections.pop(connection[0])
        print(self.msgs["user_left"].format(now(), connection[0]))
        self.send_to_all('!list ' + ' '.join(self.userlist()))


    def start(self):
        print(self.msgs["start"].format(self.__port, self.__host))
        self.socket.bind((self.__host, self.__port))
        self.socket.listen(10)
        while True:
            client_socket, address=self.socket.accept()
            nickname = self.auth(client_socket)
            self.connections[nickname]=[nickname, client_socket]
            self.send_to_all('!list '+' '.join(self.userlist()))
            print(self.msgs["connect"].format(now(),nickname,address) )
            threading.Thread(target=self.client_handle, args=( self.connections[nickname],)).start()

    def auth(self, connection):
        connection.send(self.msgs["welcome"].encode())
        data=connection.recv(100)
        nickname=data.decode('utf-8')
        return nickname

    def send_to_all(self, msg):
        for conn in self.connections.values():
            conn[1].send(msg.encode())

    def send_to_user(self, touser, msg):
        self.connections[touser][1].send(self.msgs["send_pm"].format(self.connections[touser][0],msg).encode())


    def client_handle(self, connection):
        while True:
            try:
                data = connection[1].recv(1024)
            except ConnectionResetError:
                break
            if not data: break
            data=data.decode('utf-8')
            check=data.split(' ')[0].rstrip(',')
            msg=' '.join(data.split(' ')[1:])
            if check[0]=='@':
                self.send_to_user( check[1:], msg )
                self.db.insert(name_from=connection[0], name_to=check[1:], message=msg)
            else:
                self.send_to_all(self.msgs["send_to_all"].format(connection[0], data))
                self.db.insert(name_from=connection[0], name_to='all', message=msg)
        self.close_connection(connection)

if __name__=="__main__":
    server=ChatServer()
    server.start()
