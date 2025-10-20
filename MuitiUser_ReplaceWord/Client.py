import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox, filedialog

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
        tk.Button(entry_frame, text="Update File", command=self.update_file).pack(side=tk.LEFT, padx=(5,0))

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

    # ------------------ File Update Function ------------------ #
    def update_file(self):
        # Step 1: Select file
        filepath = filedialog.askopenfilename(title="Select File")
        if not filepath:
            return

        # Step 2: Enter word to replace
        word_to_replace = simpledialog.askstring("Word to Replace", "Enter the word to replace:")
        if not word_to_replace:
            return

        # Step 3: Enter replacement word
        replacement_word = simpledialog.askstring("Replacement Word", "Enter the replacement word:")
        if replacement_word is None:
            return

        try:
            # Step 4: Read file
            with open(filepath, 'r') as f:
                content = f.read()

            # Step 5: Replace word
            modified_content = content.replace(word_to_replace, replacement_word)

            # Step 6: Write back to file
            with open(filepath, 'w') as f:
                f.write(modified_content)

            # Step 7: Show confirmation in chat
            self.insert_message(
                f"File '{filepath}' updated: '{word_to_replace}' replaced by '{replacement_word}'",
                "right"
            )

        except Exception as e:
            messagebox.showerror("File Error", str(e))

    # ------------------ Closing Function ------------------ #
    def on_closing(self):
        try:
            self.client_socket.close()
        except:
            pass
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()
