#!/usr/bin/env python3
# -*- coding: utf-8  -*-
import  sys
from string import  ascii_lowercase
from  random import choice, randint
import threading, socket
import tkinter as tk
from tkinter.ttk import *



def make_nickname():
    return ''.join([choice(ascii_lowercase) for x in range(randint(5,10))])





class Client(object):

    def __init__(self, nickname, chatframe, userframe, host='localhost', port=6777):
        self.nickname=nickname
        self.chatframe = chatframe
        self.usersframe = userframe
        self.__host = host
        self.__port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self):
        try:
            self.socket.connect((self.__host, self.__port))
            self.socket.recv(100)
            self.socket.send(self.nickname.encode())
        except:
            return (0, 'Can not connect to the server...\r\n')
        else:
            return (1, 'Connected to the server...\r\n')


    def chat_loop(self):
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            if data.decode().split()[0]=='!list':
                self.updatelist(data.decode())
            else:
                self.chatframe.insert(tk.END, data.decode('utf-8') + '\r\n')
        self.socket.close()

    def send_message(self, msg):
        self.socket.send(msg.encode())

    def updatelist(self, users):
        users=users.rstrip().split(' ')[1:]
        self.usersframe.delete('1.0',tk.END)
        for user in users:
            self.usersframe.insert(tk.END, user+ '\n')



def select_user(event, user, message):
    message.delete(0,tk.END)
    if len(user)<=2:
        return
    message.insert(tk.END, '@'+user+', ')
    message.focus()

def send_message(clientobj, msg_window):
    client.send_message(message.get())
    msg_window.delete(0,tk.END)

#TODO make settings
def settings(x,y):
    dialog = tk.Toplevel()
    dialog.geometry('260x200')
    dialog.geometry('+' + str(x + 50) + '+' + str(y + 50))
    dialog.title('Settings')
    dialog.grab_set()
    tk.Label(dialog, text='nickname').place(x=30, y=30)
    tk.Label(dialog, text='server port').place(x=30, y=60)
    tk.Label(dialog, text='server host').place(x=30, y=90)
    name=tk.Entry(dialog)
    port=tk.Entry(dialog)
    host=tk.Entry(dialog)
    name.place(x=100, y=30)
    port.place(x=100, y=60)
    host.place(x=100, y=90)
    tk.Button(dialog, text='Apply', ).place(x=100, y=170)
    tk.Button(dialog, text='Close', command=dialog.destroy).place(x=150, y=170)

main_window = tk.Tk()
main_window.style = Style() # try to use more modern window style if possible
main_window.style.theme_use('default')
main_window.geometry('500x550')
main_window.title('Simple chat')
menu=tk.Menu()
menu.add_command(label='Settings', command=lambda :settings(main_window.winfo_x(),main_window.winfo_y()))
main_window.config(menu=menu)
chat = tk.Text(main_window, height=26, width=43, font='Arial 10 normal', wrap=tk.WORD)
userlist = tk.Text(main_window, height=26, width=15, font='Arial 10 normal', wrap=tk.WORD)
message = Entry(main_window, font='Arial 10 normal', width=40)
btn_send = Button(main_window, text="Send", command=lambda: send_message(client, message))
order = userlist.bindtags()
userlist.bindtags((order[1], order[0], order[2], order[3]))
message.bind('<Return>', lambda e: send_message(client, message) )
userlist.bind('<Double-Button-1>', lambda e: select_user(e, userlist.selection_get(), message))
message.focus()
chat.place(x=35, y=30)
userlist.place(x=365, y=30)
message.place(x=35, y=470)
btn_send.place(x=280, y=466)

client = Client(make_nickname(), chat, userlist)
conn=client.start()
if conn[0]:
    threading.Thread(target=client.chat_loop, daemon=True).start()
else:
    chat.insert(tk.END, conn[1])
main_window.mainloop()
