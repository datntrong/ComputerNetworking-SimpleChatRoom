import os
import threading
import socket
import tkinter as tk

class Server(threading.Thread):
    """
    Quản lý các kết nối của server.

    Attributes:
        connections (list): Danh sách các đối tượng ServerSocket đại diện cho các client kết nối đến server.
        host (str): Địa chỉ IP của server.
        port (int): Port của server.
    """

    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        """
        Tạo một socket để lắng nghe các. Sokcet sử  dụng SO_REUSEADDR để cho phép các client
        liên kết với một địa chỉ socket đã được sử dụng trước đó.
        Với mỗi kết nối mới, một luồng ServerSocket sẽ được bắt đầu đễ dễ dàng kết nối với
        server. Tất cả đối tượng ServerSocket được lưu trong connections.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print('Listening at', sock.getsockname())

        while True:
            # Nhận một kết nối mới
            sc, sockname = sock.accept()
            print('Accepted a new connection from {} to {}'.format(sc.getpeername(), sc.getsockname()))

            # Tạo luồng
            server_socket = ServerSocket(sc, sockname, self)

            # Bắt đầu luồng mới
            server_socket.start()

            # Thêm luồng mới vào connections
            self.connections.append(server_socket)
            print('Ready to receive messages from', sc.getpeername())

    def broadcast(self, message, source):
        """
        Gửi tin nhắn tới tất cả các client, trừ người gửi tin.

        Args:
            message (str): Tin nhắn.
            source (tuple): Địa chỉ người gửi.
        """

        for connection in self.connections:

            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):
        """
        Xoá một luồng ServerSocket ở connections.

        Args:
            connection (ServerSocket): Luồng ServerSocket cần xoá.
        """
        self.connections.remove(connection)


class ServerSocket(threading.Thread):
    """
    Giao tiếp với một client đã kết nối.

    Attributes:
        sc (socket.socket): Socker kết nối.
        sockname (tuple): Địa chỉ của client.
        server (Server): Luồng server.
    """
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server

    def run(self):
        """
        Nhận dữ liệu từ client và gửi tin tới các client khác 
        Nếu một client rời phòng chat, đóng kết nối socket và xoá ServerSocket cuả nó.
        """
        while True:
            message = self.sc.recv(1024).decode('ascii')
            if message:
                print('{} says {!r}'.format(self.sockname, message))
                self.server.broadcast(message, self.sockname)
            else:
                # Client has closed the socket, exit the thread
                print('{} has closed the connection'.format(self.sockname))
                self.sc.close()
                self.server.remove_connection(self)
                return

    def send(self, message):
        """
        Gửi tin nhắn tới các kết nối
        Args:
            message (str): Tin nhắn.
        """
        self.sc.sendall(message.encode('ascii'))


# def exit(server):
#     while True:
#         ipt = input('')
#         if ipt == 'q':
#             print('Closing all connections...')
#             for connection in server.connections:
#                 connection.sc.close()
#             print('Shutting down the server...')
#             os._exit(0)

class App:
    def __init__(self):
        self.host = None
        self.port = None
        self.server = None
    def start(self):
        root = tk.Tk()
        root.title("Server")
        root.geometry("300x250")

        host_lb = tk.Label(root, text="HOST").place(x=30, y=50)
        port_lb = tk.Label(root, text="PORT").place(x=30, y=90)




        start_btn = tk.Button(root, text="Start", command=lambda: self.get_str_host_port(host_input, port_input, root))
        start_btn.place(x=30, y=170)

        host_input = tk.Entry(root)
        host_input.place(x=80, y=50)
        host_input.insert(0, "127.0.0.1")

        port_input = tk.Entry(root)
        port_input.place(x=80, y=90)
        port_input.insert(0, "1060")

        quit_btn = tk.Button(root, text="Quit", command=lambda: self.quit())
        quit_btn.place(x=80,y=170)

        root.mainloop()

    def get_str_host_port(self, host_input, port_input, root):
        self.host = host_input.get()
        self.port = port_input.get()
        self.host = str(self.host)
        self.port = int(self.port)
        self.run()
    def run(self):
        self.server = Server(host=self.host, port=self.port)
        self.server.start()
    def quit(self):
        exit = threading.Thread(target=self.exit)
        exit.start()
    def exit(self):
        print('Closing all connections...')
        for connection in self.server.connections:
            connection.sc.close()
        print('Shutting down the server...')
        os._exit(0)


if __name__ == '__main__':
    app = App()
    app.start()
    
