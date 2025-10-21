import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

class PalindromeClient:
    def __init__(self, master):
        self.master = master
        master.title("Palindrome Client")

        # Chat/Text area
        self.text_area = scrolledtext.ScrolledText(master, width=60, height=20, state='disabled')
        self.text_area.pack(padx=10, pady=5)

        # Input field
        self.entry_msg = tk.Entry(master, width=50)
        self.entry_msg.pack(side=tk.LEFT, padx=(10,5), pady=5)
        self.entry_msg.bind("<Return>", self.send_text)

        self.send_btn = tk.Button(master, text="Send", command=self.send_text)
        self.send_btn.pack(side=tk.LEFT, padx=(0,10), pady=5)

        # Connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(("127.0.0.1", 6000))
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            master.quit()
            return

        threading.Thread(target=self.receive_response, daemon=True).start()

    def send_text(self, event=None):
        text = self.entry_msg.get()
        if text:
            try:
                self.client_socket.send(text.encode())
                self.entry_msg.delete(0, tk.END)
                self.append_text(f"Sent: {text}\n", "black")
            except Exception as e:
                messagebox.showerror("Send Error", str(e))

    def receive_response(self):
        while True:
            try:
                data = self.client_socket.recv(4096).decode()
                if not data:
                    break
                self.append_text(f"Server Response:\n{data}\n\n", "blue")
            except:
                break

    def append_text(self, msg, color="black"):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, msg)
        self.text_area.tag_add(color, "end-1l linestart", "end-1l lineend")
        self.text_area.tag_config(color, foreground=color)
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    def on_closing(self):
        try:
            self.client_socket.close()
        except:
            pass
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    client = PalindromeClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()
