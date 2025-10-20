import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox, filedialog

class ChatClient:
    def __init__(self, master):
        self.master = master
        master.title("TCP Chat Client")

        self.username = simpledialog.askstring("Username", "Enter your name", parent=master)
        if not self.username:
            messagebox.showerror("Error", "Username required")
            master.quit()
            return

        # Chat area
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=50, height=20)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.tag_configure("left", justify="left", foreground="black")
        self.text_area.tag_configure("right", justify="right", foreground="blue")

        # Message entry
        entry_frame = tk.Frame(master)
        entry_frame.pack(padx=10, pady=5)
        self.entry_msg = tk.Entry(entry_frame, width=40)
        self.entry_msg.pack(side=tk.LEFT)
        self.entry_msg.bind("<Return>", self.send_message)
        tk.Button(entry_frame, text="Send", command=self.send_message).pack(side=tk.LEFT, padx=(5, 0))

        # File word replacement
        file_frame = tk.Frame(master)
        file_frame.pack(padx=10, pady=10)
        tk.Button(file_frame, text="Select File", command=self.select_file).pack(side=tk.LEFT)
        tk.Label(file_frame, text="Word to replace:").pack(side=tk.LEFT, padx=(10,0))
        self.old_word_entry = tk.Entry(file_frame, width=10)
        self.old_word_entry.pack(side=tk.LEFT, padx=(0,5))
        tk.Label(file_frame, text="New word:").pack(side=tk.LEFT)
        self.new_word_entry = tk.Entry(file_frame, width=10)
        self.new_word_entry.pack(side=tk.LEFT, padx=(0,5))
        tk.Button(file_frame, text="Replace Word", command=self.replace_word_in_file).pack(side=tk.LEFT, padx=(5,0))

        self.selected_file = None

        # Socket connection
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

    # ---------------- File word replacement -----------------
    def select_file(self):
        self.selected_file = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text Files", "*.txt")])
        if self.selected_file:
            messagebox.showinfo("File Selected", f"Selected file: {self.selected_file}")

    def replace_word_in_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected!")
            return

        old_word = self.old_word_entry.get()
        new_word = self.new_word_entry.get()
        if not old_word or not new_word:
            messagebox.showerror("Error", "Both words are required!")
            return

        try:
            with open(self.selected_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content.replace(old_word, new_word)

            with open(self.selected_file, "w", encoding="utf-8") as f:
                f.write(new_content)

            messagebox.showinfo("Success", f"Replaced '{old_word}' with '{new_word}' in file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to replace word: {str(e)}")

    # ---------------- Closing -----------------
    def on_closing(self):
        try: self.client_socket.close()
        except: pass
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()
