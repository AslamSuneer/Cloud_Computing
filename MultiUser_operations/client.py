import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox, filedialog
from collections import Counter

class ChatClient:
    def __init__(self, master):
        self.master = master
        master.title("TCP Chat Client")

        # Username input
        self.username = simpledialog.askstring("Username", "Enter your name", parent=master)
        if not self.username:
            messagebox.showerror("Error", "Username required")
            master.quit()
            return

        # Chat area
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.tag_configure("left", justify="left", foreground="black")
        self.text_area.tag_configure("right", justify="right", foreground="blue")

        # Entry and buttons
        entry_frame = tk.Frame(master)
        entry_frame.pack(padx=10, pady=5)

        self.entry_msg = tk.Entry(entry_frame, width=40)
        self.entry_msg.pack(side=tk.LEFT)
        self.entry_msg.bind("<Return>", self.send_message)

        tk.Button(entry_frame, text="Send", command=self.send_message).pack(side=tk.LEFT, padx=(5,0))
        tk.Button(entry_frame, text="File Menu", command=self.file_menu).pack(side=tk.LEFT, padx=(5,0))

        # Connect to server
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('127.0.0.1', 5000))
            self.client_socket.send(self.username.encode())
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            master.quit()
            return

        threading.Thread(target=self.receive_messages, daemon=True).start()

    # ------------------ Chat Functions ------------------ #
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

    # ------------------ File Menu ------------------ #
    def file_menu(self):
        win = tk.Toplevel(self.master)
        win.title("File Operations")

        tk.Button(win, text="Replace Word", command=self.replace_word).pack(padx=10, pady=5)
        tk.Button(win, text="Character Count", command=self.char_count).pack(padx=10, pady=5)
        tk.Button(win, text="Line Count", command=self.line_count).pack(padx=10, pady=5)
        tk.Button(win, text="Find Frequent Words", command=self.frequent_words).pack(padx=10, pady=5)
        tk.Button(win, text="Sort Data", command=self.sort_data).pack(padx=10, pady=5)
        tk.Button(win, text="Sum/Average/Min/Max", command=self.stats_numbers).pack(padx=10, pady=5)

    # ------------------ 1. Replace Word ------------------ #
    def replace_word(self):
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath: return

        word_to_replace = simpledialog.askstring("Word to Replace", "Enter the word to replace:")
        replacement_word = simpledialog.askstring("Replacement Word", "Enter the replacement word:")
        if not word_to_replace or replacement_word is None: return

        try:
            with open(filepath, 'r') as f:
                content = f.read()
            modified_content = content.replace(word_to_replace, replacement_word)
            with open(filepath, 'w') as f:
                f.write(modified_content)

            msg = f"updated: replaced '{word_to_replace}' with '{replacement_word}' in {filepath}"
            self.insert_message(f"✅ {msg}", "right")
            self.client_socket.send(msg.encode())

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------ 2. Character Count ------------------ #
    def char_count(self):
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath: return
        with open(filepath, 'r') as f:
            content = f.read()
        count = len(content)

        msg = f"analyzed: character count {count} in {filepath}"
        self.insert_message(f"📊 {msg}", "right")
        self.client_socket.send(msg.encode())

    # ------------------ 3. Line Count ------------------ #
    def line_count(self):
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath: return
        with open(filepath, 'r') as f:
            lines = f.readlines()

        msg = f"analyzed: line count {len(lines)} in {filepath}"
        self.insert_message(f"📊 {msg}", "right")
        self.client_socket.send(msg.encode())

    # ------------------ 4. Frequent Words ------------------ #
    def frequent_words(self):
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath: return
        with open(filepath, 'r') as f:
            words = f.read().split()
        freq = Counter(words)
        top_5 = freq.most_common(5)

        msg = f"analyzed: top 5 frequent words {top_5} in {filepath}"
        self.insert_message(f"🔥 {msg}", "right")
        self.client_socket.send(msg.encode())

    # ------------------ 5. Sort Data ------------------ #
    def sort_data(self):
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath: return
        with open(filepath, 'r') as f:
            lines = f.readlines()
        lines_sorted = sorted(lines)
        with open(filepath, 'w') as f:
            f.writelines(lines_sorted)

        msg = f"updated: sorted file {filepath} alphabetically"
        self.insert_message(f"✅ {msg}", "right")
        self.client_socket.send(msg.encode())

    # ------------------ 6. Stats (Sum/Average/Min/Max) ------------------ #
    def stats_numbers(self):
        filepath = filedialog.askopenfilename(title="Select Numeric File")
        if not filepath: return
        try:
            with open(filepath, 'r') as f:
                numbers = [float(x) for x in f.read().split()]

            s = sum(numbers)
            avg = s / len(numbers)
            mn = min(numbers)
            mx = max(numbers)

            msg = f"analyzed: stats Sum={s}, Avg={avg:.2f}, Min={mn}, Max={mx} in {filepath}"
            self.insert_message(f"📈 {msg}", "right")
            self.client_socket.send(msg.encode())
        except Exception as e:
            messagebox.showerror("File Error", f"Not numeric data: {e}")

    # ------------------ Closing Function ------------------ #
    def on_closing(self):
        try:
            self.client_socket.close()
        except: pass
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()
