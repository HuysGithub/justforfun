import tkinter as tk
from tkinter import Label, Button

import socket
import threading, json 
import time

class HomePage(tk.Tk):
    def __init__(self, profile, socket: socket.socket = None):
        super().__init__()
        self.profile = profile
        self.socket = socket
        self.send_form = {"type": None, "money": 0}
        
        self.time_label = Label(self)
        time_label_text = Label(self.time_label,text="time")
        time_label_text.grid(row=0,column=0, padx=10, pady=10)
        self.time_label_value = Label(self.time_label,text='0')
        self.time_label_value.grid(row=0,column=2, padx=10, pady=10)
        self.time_label.pack()
        
        self.username_label = Label(self)
        username_label_text = Label(self.username_label,text="username")
        username_label_text.grid(row=1,column=0, padx=10, pady=10)
        username_label_value = Label(self.username_label,text=self.profile["username"])
        username_label_value.grid(row=1,column=2, padx=10, pady=10)
        self.username_label.pack()
        
        self.balance_label = Label(self)
        balance_label_text = Label(self.balance_label,text="balance")
        balance_label_text.grid(row=2,column=0, padx=10, pady=10)
        self.balance_label_value = Label(self.balance_label,text=self.profile["balance"])
        self.balance_label_value.grid(row=2,column=2, padx=10, pady=10)
        self.balance_label.pack()
        
        self.yourChoose_label = Label(self)
        yourChoose_label_text = Label(self.yourChoose_label,text="Your Choose: ")
        yourChoose_label_text.grid(row=3,column=0, padx=10, pady=10)
        self.yourChoose_label_value = Label(self.yourChoose_label,text="None")
        self.yourChoose_label_value.grid(row=3,column=2, padx=10, pady=10)
        self.yourChoose_label.pack()
        
        self.money_label = Label(self)
        money_label_text = Label(self.money_label,text="Cuoc: ")
        money_label_text.grid(row=4,column=0, padx=10, pady=10)
        self.money_label_value = Label(self.money_label,text=self.send_form["money"])
        self.money_label_value.grid(row=4,column=2, padx=10, pady=10)
        self.money_label.pack()
        
        self.result_label = Label(self, text="Result:")
        self.result_label.pack()
        
        self.tx_label = Label(self)
        tai_button = Button(self.tx_label, text="TAI", command=self.on_tai_click)
        tai_button.grid(row=0, column=0, padx=10, pady=10)
        xiu_button = Button(self.tx_label, text="reset", command=self.on_reset_click)
        xiu_button.grid(row=0,column=1, padx=10, pady=10)
        xiu_button = Button(self.tx_label, text="XIU", command=self.on_xiu_click)
        xiu_button.grid(row=0,column=2, padx=10, pady=10)
        self.tx_label.pack()
        
        self.moneyzone_label = tk.Frame(self)
        
        amounts = [10000, 20000, 50000, 100000, 200000, 500000]

        for i, amount in enumerate(amounts):
            row = i // 3
            col = i % 3
            button_text = f"{amount:,}"
            button = Button(self.moneyzone_label, text=button_text, command=lambda amt=amount: self.on_button_click(amt))
            button.grid(row=row, column=col, padx=10, pady=10)
            
        self.moneyzone_label.pack()
        time.sleep(1)
        threading.Thread(target=self.handle_server_message).start()
        self.mainloop()
        
    def update_balance(self, balance):
        self.profile["balance"] = balance
        self.balance_label_value.config(text=balance)

    def handle_server_message(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                message = json.loads(data)
                print("recv from server" + str(message))
                if "status" in message:
                    # Nếu nhận được thông điệp từ máy chủ về trạng thái
                    countdown_time = message["status"]
                    if countdown_time == 0:
                        threading.Thread(target=self.send).start()
                        
                    else:
                        threading.Thread(target=self.update_countdown, args=(countdown_time,)).start()

                elif "result" in message:
        
                    result = message["result"]
                    balance = message["balance"]
                    self.update_balance(balance)
                    number = message["number"]
                    if result == None:
                        self.result_label.config(text=f"Result: {number}")
                    elif result == True:
                        self.result_label.config(text=f"Result: {number} You win!")
                    else:
                        self.result_label.config(text=f"Result: {number} You lost!")
                    
            except Exception as e:
                print("Error while receiving message from server:", e)
                break

        
    def send(self):
        content = json.dumps(self.send_form)
        self.socket.send(content.encode())
        print("send to server: " + str(content))
        self.on_reset_click()
        

    def update_countdown(self, start_time):
        for i in range(start_time, 0, -1):
            self.time_label_value.config(text=i)
            time.sleep(1)

    def on_button_click(self, amount):
        if self.profile["balance"] >= (self.send_form["money"] + amount):
            self.send_form["money"] += amount
            self.money_label_value.configure(text=self.send_form["money"])
        
    def on_tai_click(self):
        self.yourChoose_label_value.configure(text="Tai")
        self.send_form["type"] = "tai"
    
    def on_xiu_click(self):
        self.yourChoose_label_value.configure(text="Xiu")
        self.send_form["type"] = "xiu"
    
    def on_reset_click(self):
        self.yourChoose_label_value.configure(text="None")
        self.money_label_value.configure(text="0")
        self.send_form["type"] = None
        self.send_form["money"] = 0
        