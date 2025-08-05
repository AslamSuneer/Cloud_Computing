import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

class ChatClient:
    def __init__(self, master):
        self.master = master
        master.title("TCP Chat Client")

        self.username = simpledialog.askstring("Username", "Enter your name", parent=master)
        if not self.username:
            messagebox.showerror("Error", "Username required")
            master.quit()
            return

        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=50, height=20)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.tag_configure("left", justify="left", foreground="black")
        self.text_area.tag_configure("right", justify="right", foreground="blue")

        entry_frame = tk.Frame(master)
        entry_frame.pack(padx=10, pady=5)
        self.entry_msg = tk.Entry(entry_frame, width=40)
        self.entry_msg.pack(side=tk.LEFT)
        self.entry_msg.bind("<Return>", self.send_message)
        tk.Button(entry_frame, text="Send", command=self.send_message).pack(side=tk.LEFT, padx=(5, 0))

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('127.0.0.1', 5000))
            self.client_socket.send(self.username.encode())
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            master.quit()
            return

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        msg = self.entry_msg.get()
        if msg:
            try:
                self.client_socket.send(msg.encode())
                self.insert_message(msg, "right")
                self.entry_msg.delete(0, tk.END)
            except:
                messagebox.showerror("Send Error", "Failed to send message")
                self.master.quit()

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode()
                self.insert_message(msg, "left")
            except:
                break

    def insert_message(self, msg, side):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, msg + "\n", side)
        self.text_area.yview_moveto(1)
        self.text_area.config(state='disabled')

    def on_closing(self):
        try: self.client_socket.close()
        except: pass
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()
