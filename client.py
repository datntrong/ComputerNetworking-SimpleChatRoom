import threading
import socket
import argparse
import os
import sys
import tkinter as tk
from modulconnetdb import *
import datetime


class Send(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            # Type 'QUIT' to leave the chatroom
            if message == 'QUIT':
                self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
                break

            # Send message to server for broadcasting
            else:
                self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))

        print('\nQuitting...')
        self.sock.close()
        os._exit(0)


class Receive(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):

        while True:
            message = self.sock.recv(1024).decode('ascii')

            if message:

                if self.messages:
                    self.messages.insert(tk.END, message)
                    print('hi')
                    print('\r{}\n{}: '.format(message, self.name), end='')

                else:
                    # Thread has started, but client GUI is not yet ready
                    print('\r{}\n{}: '.format(message, self.name), end='')

            else:
                # Server has closed the socket, exit the program
                print('\nOh no, we have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None

    def start(self):

        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Successfully connected to {}:{}'.format(self.host, self.port))

        print()
        self.name = input('Your name: ')

        print()
        print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))

        # Create send and receive threads
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        # Start send and receive threads
        send.start()
        receive.start()

        self.sock.sendall('Server: {} has joined the chat. Say hi!'.format(self.name).encode('ascii'))
        print("\rAll set! Leave the chatroom anytime by typing 'QUIT'\n")
        print('{}: '.format(self.name), end='')

        return receive

    def load_old_message(self):
        arr_messages = arr_message()
        for i in arr_messages:
            message = i
            self.messages.insert(tk.END, '{}: {}'.format(message[0], message[1]))

    def send(self, text_input):

        message = text_input.get()
        text_input.delete(0, tk.END)
        self.messages.insert(tk.END, '{}: {}'.format(self.name, message))

        # Type 'QUIT' to leave the chatroom
        if message == 'QUIT':
            self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))

            print('\nQuitting...')
            self.sock.close()
            os._exit(0)

        # Send message to server for broadcasting
        else:
            datetime_object = datetime.datetime.now()
            stri = str(datetime_object)
            t = stri.split('.')
            datetime_str = t[0]
            # insert_message(self.name, message, datetime_str)
            self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))


class App:
    def __init__(self, root, host, port):
        self.client = Client(host, port)
        receive = self.client.start()
        root.title('Chatroom')
        root.rowconfigure(0, minsize=500, weight=1)
        root.rowconfigure(1, minsize=50, weight=0)
        root.columnconfigure(0, minsize=500, weight=1)
        root.columnconfigure(1, minsize=200, weight=0)

        # menu

        """
        menubar = tk.Menu(root)
        file = tk.Menu(menubar, tearoff=0)
        file.add_command(label="New")
        file.add_command(label="Open")
        file.add_command(label="Save")
        file.add_command(label="Save as...")
        file.add_command(label="Close")

        file.add_separator()

        file.add_command(label="Exit", command=root.quit)

        menubar.add_cascade(label="File", menu=file)
        edit = tk.Menu(menubar, tearoff=0)
        edit.add_command(label="Undo")

        edit.add_separator()

        edit.add_command(label="Cut")
        edit.add_command(label="Copy")
        edit.add_command(label="Paste")
        edit.add_command(label="Delete")
        edit.add_command(label="Select All")

        menubar.add_cascade(label="Edit", menu=edit)
        help = tk.Menu(menubar, tearoff=0)
        help.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help)

        root.config(menu=menubar)
        root.mainloop()
        """


        frm_messages = tk.Frame(master=root)
        scrollbar = tk.Scrollbar(master=frm_messages)
        messages = tk.Listbox(
            master=frm_messages,
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #
        self.client.messages = messages
        receive.messages = messages

        frm_messages.grid(row=20, column=50, columnspan=2, sticky="nsew")

        frm_entry = tk.Frame(master=root)
        text_input = tk.Entry(master=frm_entry)
        text_input.pack(fill=tk.BOTH, expand=True)
        self.client.load_old_message()
        text_input.bind("<Return>", lambda x: self.client.send(text_input))
        text_input.insert(0, "Your message here.")

        btn_send = tk.Button(
            master=root,
            text='Send',
        )
        btn_send["command"] = lambda: self.command_btn_send(text_input)
        frm_entry.grid(row=1, column=0, padx=10, sticky="ew")
        btn_send.grid(row=1, column=1, pady=10, sticky="ew")

    def command_btn_send(self, text_input):
        self.client.send(text_input)
    def donothing(self):
        print("a")
def main(host, port):
    create_database()
    root = tk.Tk()
    app = App(root, host, port)
    root.mainloop()


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 1060
    main(HOST, PORT)