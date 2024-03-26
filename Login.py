import tkinter as tk
from tkinter import Label, Entry, Button
import socket
import json

class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x300")
        self.status = False
        self.user = {}
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # UI
        Label(self, text="username").pack()
        self.username_entry = Entry(self)
        self.username_entry.pack()
        
        Label(self, text="password").pack()
        self.password_entry = Entry(self, show="*")
        self.password_entry.pack()
        
        Label(self, text="Host").pack()
        self.host_entry = Entry(self)
        self.host_entry.pack()
        
        Label(self, text="Port").pack()
        self.port_entry = Entry(self)
        self.port_entry.pack()
        
        self.notion_label = Label(self, text="")
        self.notion_label.pack()
        self.login_button = Button(self, text="Login", command=lambda:self.on_click_login())
        self.login_button.pack()
        
        self.mainloop()
        
    def on_click_login(self):
        server_address = (self.host_entry.get(), int(self.port_entry.get()))
        
        self.client_socket.connect(server_address)
        self.user = {"username":self.username_entry.get(),
                    "password": self.password_entry.get()}
        # tạo json
        
        data = json.dumps(self.user)
        
        # gửi chuỗi json đã encode
        self.client_socket.send(data.encode())
        
        
        response = self.client_socket.recv(2048)
        print(response)
        print(response.decode())
        self.user = json.loads(response)
        print(self.user)
        if self.user == {}:  # Kiểm tra xem dữ liệu trả về có rỗng không
            self.notion_label.configure(text="username or password not correct")
            return
        else:
            self.destroy()

        
    def connect_to_server(self):
        if self.client_socket:
            self.client_socket.close()
        