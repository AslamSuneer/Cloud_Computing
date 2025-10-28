import socket
import threading

# -----------------------------
# Quiz questions and answers
# -----------------------------
quiz_data = [
    ("What is the capital of France?", "paris"),
    ("What is 5 + 7?", "12"),
    ("Which planet is known as the Red Planet?", "mars"),
    ("Who wrote 'Hamlet'?", "shakespeare"),
    ("What is the square root of 64?", "8")
]

HOST = '127.0.0.1'   # Localhost (loopback)
PORT = 5000          # Port number for TCP connection

# -----------------------------
# Function to handle each client
# -----------------------------
def handle_client(conn, addr):
    print(f"[+] Connected to {addr}")
    score = 0  # Initialize client's score

    try:
        # Loop through each quiz question
        for i, (question, answer) in enumerate(quiz_data, start=1):
            # Send the question to the client
            conn.sendall(f"Q{i}: {question}".encode())

            # Set 10-second timeout for client's answer
            conn.settimeout(10.0)

            try:
                # Receive client's answer
                data = conn.recv(1024).decode().strip().lower()
            except socket.timeout:
                # If the client takes too long to answer
                conn.sendall("Time out! No answer received.\n".encode())
                continue

            # -----------------------------
            # Check if answer is correct
            # -----------------------------
            if data == answer:
                score += 10  # Add 10 points for correct answer
                conn.sendall("Correct!\n".encode())
                print(f"[{addr}] Q{i}: Correct Answer ✅ ({data})")
            else:
                conn.sendall(f"Wrong! Correct answer: {answer}\n".encode())
                print(f"[{addr}] Q{i}: Wrong ❌ (Given: {data}, Expected: {answer})")

        # Send final score to client
        conn.sendall(f"Quiz finished! Your score: {score}/50\n".encode())
        print(f"[SCORE] {addr} -> {score}/50")

    except (ConnectionResetError, BrokenPipeError):
        print(f"[DISCONNECTED] {addr} abruptly disconnected.")

    finally:
        conn.close()
        print(f"[-] Connection closed with {addr}")

# -----------------------------
# Start the TCP server
# -----------------------------
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

        try:
            while True:
                # Wait for client connection
                conn, addr = server.accept()

                # Handle client in a new thread
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
        except KeyboardInterrupt:
            print("\n[SERVER STOPPED] Shutting down.")

# Run the server
if __name__ == "__main__":
    start_server()
