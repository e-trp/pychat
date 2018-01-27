#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import threading, time, socket

def now():
    return time.ctime(time.time())

class ChatServer(object):

    def __init__(self, host='localhost', port=6777):
        self.__host=host
        self.__port=port
        self.connections=[]        #[ username, socket ]
        self.commands=dict()
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def userlist(self):
        return [conn[0] for conn in self.connections]

    def close_connection(self, client):
        for i, conn in enumerate(self.connections):
            if client is conn[1]:
                self.connections.pop(i)
                print("{} user '{}' left from chat".format(now(), conn[0]))
        client.close()
        self.send_to_all('!list ' + ' '.join(self.userlist()))


    def start(self):
        print("Starting server on port {} and host '{}'\n".format(self.__port, self.__host))
        self.socket.bind((self.__host, self.__port))
        self.socket.listen(10)
        while True:
            client_socket, address=self.socket.accept()
            nickname = self.auth(client_socket)
            connection=[nickname, client_socket]
            self.connections.append(connection)
            self.send_to_all('!list '+' '.join(self.userlist()))
            print("{} user '{}'{} connected".format(now(),nickname,address) )
            threading.Thread(target=self.client_handle, args=(connection,)).start()

    def auth(self, connection):
        connection.send('Welcome to chat server, please enter your nickname: \r\n'.encode()
        )
        data=connection.recv(100)
        nickname=data.decode('utf-8')
        return nickname

    def send_to_all(self, msg):
        for i, conn in enumerate(self.connections):
            conn[1].send(msg.encode())

    def send_to_user(self, fromuser, touser, msg):
        msg='pm {} : {}'.format(fromuser, msg)
        for username, conn  in self.connections:
            if touser==username:
                conn.send(msg.encode())



    def client_handle(self,connection):
        while True:
            try:
                data = connection[1].recv(1024)
            except ConnectionResetError:
                break
            if not data: break
            data=data.decode('utf-8')
            print(data)
            check=data.split(' ')[0].rstrip(',')
            if check[0]=='@':
                self.send_to_user(connection[0], check[1:], ' '.join(data.split(' ')[1:]) )
            else:
                self.send_to_all("{}: {}".format(connection[0], data))
        self.close_connection(connection[1])

if __name__=="__main__":
    server=ChatServer()
    server.start()
