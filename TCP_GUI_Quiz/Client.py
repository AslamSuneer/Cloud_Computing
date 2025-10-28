import socket
import threading
import tkinter as tk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 5000

class QuizClient:
    def __init__(self, master):
        self.master = master
        self.master.title("TCP Quiz Client")
        self.master.geometry("400x300")

        # Connect to server
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conn.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Cannot connect to server: {e}")
            master.destroy()
            return

        # -----------------------------
        # GUI Elements
        # -----------------------------
        self.question_label = tk.Label(master, text="Waiting for question...", wraplength=350, font=("Arial", 12))
        self.question_label.pack(pady=20)

        self.answer_entry = tk.Entry(master, font=("Arial", 12))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(master, text="Submit", command=self.send_answer, state='disabled')
        self.submit_button.pack(pady=10)

        self.feedback_label = tk.Label(master, text="", font=("Arial", 11), fg="blue")
        self.feedback_label.pack(pady=10)

        # Flag to control message receiving loop
        self.running = True

        # Start background thread to receive server messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    # -----------------------------
    # Send answer to server
    # -----------------------------
    def send_answer(self):
        answer = self.answer_entry.get().strip()
        if answer:
            self.conn.sendall(answer.encode())
            self.answer_entry.delete(0, tk.END)
            self.submit_button.config(state='disabled')

    # -----------------------------
    # Receive messages from server
    # -----------------------------
    def receive_messages(self):
        while self.running:
            try:
                data = self.conn.recv(1024).decode()
                if not data:
                    break

                # If message starts with "Q" → it's a new question
                if data.startswith("Q"):
                    self.question_label.config(text=data)
                    self.feedback_label.config(text="")
                    self.answer_entry.config(state='normal')
                    self.submit_button.config(state='normal')

                # If quiz is finished
                elif "Quiz finished" in data:
                    self.feedback_label.config(text=data)
                    self.answer_entry.config(state='disabled')
                    self.submit_button.config(state='disabled')
                    messagebox.showinfo("Quiz Over", data)
                    self.conn.close()
                    self.running = False
                    break

                # Otherwise → feedback ("Correct!" / "Wrong!" / "Timeout")
                else:
                    self.feedback_label.config(text=data)

            except Exception as e:
                print("Connection closed:", e)
                break

# -----------------------------
# Run the GUI client
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizClient(root)
    root.mainloop()
