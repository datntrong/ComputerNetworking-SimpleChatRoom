import threading
import socket
import argparse
import os
import sys
import tkinter as tk
import webbrowser

from modulconnetdb import *
import datetime


class Send(threading.Thread):
    """
    Luồng gửi tin nhắn: lắng nghe input từ dòng lệnh của người dùng.

    Attributes:
        sock (socket.socket): Socket kết nối với server.
        name (str): username của client.
    """

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        """
        Lắng nghe input của người dùng từ dòng lệnh và gửi nó đến server.
        Gõ 'QUIT' sẽ đóng kết nối với server và thoát chương trình.
        """
        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            # Gõ 'QUIT' để rời phòng chat
            if message == 'QUIT':
                self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
                break

            # Gửi tin đến server để broadcasting
            else:
                self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))

        print('\nQuitting...')
        self.sock.close()
        os._exit(0)


class Receive(threading.Thread):
    """
    Luồng nhận tin nhắn: lắng nghe tin nhắn từ server gửi tới.

    Attributes:
        sock (socket.socket): Socket kết nối với server.
        name (str): username của client.
        messages (tk.Listbox): Đối tượng tk.Listbox gồm tất cả tin nhắn hiện trên cửa sổ chat.
    """

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):
        """
        Nhận dữ liệu từ server và hiện thị lên cửa sổ chat.
        Luôn lắng nghe dữ liệu được gửi tới đến khi socket của client hoặc server đóng. 
        """
        while True:
            message = self.sock.recv(1024).decode('ascii')

            if message:

                if self.messages:
                    self.messages.insert(tk.END, message)
                    print('hi')
                    print('\r{}\n{}: '.format(message, self.name), end='')

                else:
                    # Bắt đầu luồng mới nhưng GUI chưa xuất hiện
                    print('\r{}\n{}: '.format(message, self.name), end='')

            else:
                # Server đã đóng socket, thoát chương trình
                print('\nOh no, we have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)


class Client:
    """
    Quản lý các kết nối client-server và tích hợp với GUI.

    Attributes:
        host (str): Địa chỉ IP của server
        port (int): Port của server.
        sock (socket.socket): Socket kết nối với server.
        name (str): username của client.
        messages (tk.Listbox): Đối tượng tk.Listbox gồm tất cả tin nhắn hiện trên cửa sổ chat.
    """

    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.messages = None

    def start(self):
        """
        Thiết lập kết nối client-server. Nhận input của nguòw dùng,
        tạo và bắt đầu luồng gửi và nhận tin nhắn, đồng thời gửi thông báo cho các client đã kết nối.\

        Returns:
            Mội đối tượng Receive đại dịên cho luồng nhận tin.
        """

        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Successfully connected to {}:{}'.format(self.host, self.port))

        # print()
        # self.name = input('Your name: ')

        print()
        print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))

        # Tạo luồng gửi và nhận tin nhắn
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        # Bắt đầu luồng gửi và nhận tin nhắn
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
        """
        Gửi dữ liệu của text_input tới khung chat. Phương thức này phải được liên kết text_input và
         bất kỳ widgets khác để thực thi, ví dụ: buttons.
        Gõ 'QUIT' sẽ đóng kết nối với server và thoát chương trình.

        Args:
            text_input(tk.Entry): Một đối tượng tk.Entry là input của người dùng.
        """
        try:
            message = text_input.get()
            text_input.delete(0, tk.END)
        except:
            message = text_input
        self.messages.insert(tk.END, '{}: {}'.format(self.name, message))

        # Gõ 'QUIT' để rời phòng chat
        if message == 'QUIT':
            self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))

            print('\nQuitting...')
            self.sock.close()
            os._exit(0)

        # Gửi tin đến server để broadcasting
        else:
            datetime_object = datetime.datetime.now()
            stri = str(datetime_object)
            t = stri.split('.')
            datetime_str = t[0]
            insert_message(self.name, message, datetime_str)
            self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))


class App:
    def __init__(self):
        self.host1 = None
        self.port1 = None
        self.client = None
        self.receive = None
        self.user = None

    def interface(self):
        self.client = Client(self.host1, self.port1, self.user)
        self.receive = self.client.start()
        root = tk.Tk()
        root.title('Chatroom')
        root.rowconfigure(0, minsize=500, weight=1)
        root.rowconfigure(1, minsize=50, weight=0)
        root.columnconfigure(0, minsize=500, weight=1)
        root.columnconfigure(1, minsize=200, weight=0)

        # menu

        menubar = tk.Menu(root)
        file = tk.Menu(menubar, tearoff=0)
        # file.add_command(label="New")
        # file.add_command(label="Open")
        # file.add_command(label="Save")
        # file.add_command(label="Save as...")
        # file.add_command(label="Close")

        file.add_separator()

        file.add_command(label="Exit", command=lambda: self.client.send('QUIT'))

        menubar.add_cascade(label="File", menu=file)
        edit = tk.Menu(menubar, tearoff=0)
        # edit.add_command(label="Undo")

        edit.add_separator()

        # edit.add_command(label="Cut")
        # edit.add_command(label="Copy")
        # edit.add_command(label="Paste")
        edit.add_command(label="Delete", command=lambda: self.del_db(frm_messages))
        # edit.add_command(label="Select All")

        menubar.add_cascade(label="Edit", menu=edit)
        help = tk.Menu(menubar, tearoff=0)
        help.add_command(label="About", command=lambda: self.about())
        menubar.add_cascade(label="Help", menu=help)

        root.config(menu=menubar)

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
        self.receive.messages = messages

        frm_messages.grid(row=0, column=0, columnspan=2, sticky="nsew")

        frm_entry = tk.Frame(master=root)
        text_input = tk.Entry(master=frm_entry)
        text_input.pack(fill=tk.BOTH, expand=True)
        self.client.load_old_message()
        text_input.bind("<Return>", lambda x: self.client.send(text_input))
        text_input.insert(0, "Your message here.")

        btn_send = tk.Button(
            master=root,
            text='Send',
            command=lambda: self.root.destroy()
        )
        btn_send["command"] = lambda: self.command_btn_send(text_input)
        frm_entry.grid(row=1, column=0, padx=10, sticky="ew")
        btn_send.grid(row=1, column=1, pady=10, sticky="ew")
        root.mainloop()

    def command_btn_send(self, text_input):
        self.client.send(text_input)

    def del_db(self, frm_message):
        delete_database()

    def about(self):
        webbrowser.open('https://github.com/datntrong/ComputerNetworking-SimpleChatRoom')  # Go to example.com

    def get_host_port(self):

        create_database()
        root = tk.Tk()
        root.title("Client")
        root.geometry("300x250")

        host_lb = tk.Label(root, text="HOST").place(x=30, y=50)
        port_lb = tk.Label(root, text="PORT").place(x=30, y=90)
        user_lb = tk.Label(root, text="Name").place(x=30, y=130)

        submit_btn = tk.Button(root, text="Submit",
                               command=lambda: self.get_str_host_port(host_input, port_input, user_import, root))
        submit_btn.place(x=30, y=170)

        host_input = tk.Entry(root)
        host_input.place(x=80, y=50)
        host_input.insert(0, "127.0.0.1")

        port_input = tk.Entry(root)
        port_input.place(x=80, y=90)
        port_input.insert(0, "1060")

        user_import = tk.Entry(root)
        user_import.place(x=80, y=130)

        root.mainloop()

    def get_str_host_port(self, host_input, port_input, user_import, root):
        self.host1 = host_input.get()
        self.port1 = port_input.get()
        print(self.host1)
        print(type(self.host1))
        self.host1 = str(self.host1)
        self.port1 = int(self.port1)
        self.user = user_import.get()
        root.quit()
        root.destroy()


def main():
    app = App()
    app.get_host_port()
    app.interface()


if __name__ == '__main__':
    main()
