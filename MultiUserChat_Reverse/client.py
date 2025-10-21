import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("TCP Chat Client")

        # Ask for username
        self.username = simpledialog.askstring("Username", "Enter your name", parent=master)
        if not self.username:
            messagebox.showerror("Error", "Username required")
            master.quit()
            return

        # Chat display area
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.tag_configure("normal", foreground="black", justify="left")
        self.text_area.tag_configure("reverse", foreground="blue", justify="left")

        # Message entry
        entry_frame = tk.Frame(master)
        entry_frame.pack(padx=10, pady=5)

        self.entry_msg = tk.Entry(entry_frame, width=40)
        self.entry_msg.pack(side=tk.LEFT, padx=(0, 5))
        self.entry_msg.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(entry_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

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

    # -------------------- Send Message --------------------
    def send_message(self, event=None):
        msg = self.entry_msg.get()
        if msg:
            try:
                self.client_socket.send(msg.encode())
                self.entry_msg.delete(0, tk.END)
            except:
                messagebox.showerror("Send Error", "Failed to send message")
                self.master.quit()

    # -------------------- Receive Messages --------------------
    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                msg = data.decode()

                # Update GUI text box
                self.text_area.config(state='normal')
                if "→" in msg:
                    original, reversed_part = msg.split("→", 1)
                    self.text_area.insert(tk.END, original.strip() + "\n", "normal")
                    self.text_area.insert(tk.END, "→ " + reversed_part.strip() + "\n\n", "reverse")
                else:
                    self.text_area.insert(tk.END, msg + "\n", "normal")
                self.text_area.config(state='disabled')
                self.text_area.yview(tk.END)

            except Exception as e:
                print("Connection closed:", e)
                break

    def on_closing(self):
        try:
            self.client_socket.close()
        except:
            pass
        self.master.quit()

# -------------------- MAIN --------------------
if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.mainloop()
