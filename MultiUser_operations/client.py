import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox, filedialog

class ChatClient:
    def __init__(self, master):
        self.master = master
        master.title("Server-based File Operations")

        self.username = simpledialog.askstring("Username", "Enter your name:", parent=master)
        if not self.username:
            messagebox.showerror("Error", "Username required")
            master.quit()
            return

        # Text display area
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20)
        self.text_area.pack(padx=10, pady=5)

        # Buttons for operations
        tk.Button(master, text="Replace Word", command=self.replace_word).pack(padx=10, pady=2)
        tk.Button(master, text="Character Count", command=self.char_count).pack(padx=10, pady=2)
        tk.Button(master, text="Line Count", command=self.line_count).pack(padx=10, pady=2)
        tk.Button(master, text="Frequent Words", command=self.frequent_words).pack(padx=10, pady=2)
        tk.Button(master, text="Sort Data", command=self.sort_data).pack(padx=10, pady=2)
        tk.Button(master, text="Stats", command=self.stats_numbers).pack(padx=10, pady=2)

        # Connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('127.0.0.1', 5000))
            self.client_socket.send(self.username.encode())
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            master.quit()
            return

        threading.Thread(target=self.receive_result, daemon=True).start()

    # ---------------- Receive result ---------------- #
    def receive_result(self):
        while True:
            try:
                msg = self.client_socket.recv(4096).decode()
                if not msg: break
                self.append_text(msg)
            except:
                break

    def append_text(self, msg):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, msg + "\n")
        self.text_area.yview_moveto(1)
        self.text_area.config(state='disabled')

    # ---------------- Operations ---------------- #
    def replace_word(self):
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath: return
        word_to_replace = simpledialog.askstring("Word to Replace", "Enter word to replace:")
        replacement_word = simpledialog.askstring("Replacement Word", "Enter replacement:")
        if not word_to_replace or replacement_word is None: return
        msg = f"replace::{filepath}::{word_to_replace}::{replacement_word}"
        self.client_socket.send(msg.encode())

    def char_count(self):
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath: return
        msg = f"char_count::{filepath}"
        self.client_socket.send(msg.encode())

    def line_count(self):
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath: return
        msg = f"line_count::{filepath}"
        self.client_socket.send(msg.encode())

    def frequent_words(self):
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath: return
        msg = f"freq_words::{filepath}"
        self.client_socket.send(msg.encode())

    def sort_data(self):
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath: return
        msg = f"sort::{filepath}"
        self.client_socket.send(msg.encode())

    def stats_numbers(self):
        filepath = filedialog.askopenfilename(title="Select Numeric File")
        if not filepath: return
        msg = f"stats::{filepath}"
        self.client_socket.send(msg.encode())

    # ---------------- Closing ---------------- #
    def on_closing(self):
        try: self.client_socket.close()
        except: pass
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()
