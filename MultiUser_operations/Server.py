import socket
import threading
from collections import Counter

def perform_operation(msg):
    """Perform file operations on the server based on client message format"""
    try:
        tokens = msg.split("::")  # Expecting "OPERATION::filepath::other_data"
        op = tokens[0]
        filepath = tokens[1]

        if op == "replace":
            word_to_replace, replacement_word = tokens[2], tokens[3]
            with open(filepath, 'r') as f:
                content = f.read()
            content = content.replace(word_to_replace, replacement_word)
            with open(filepath, 'w') as f:
                f.write(content)
            return f" Replaced '{word_to_replace}' with '{replacement_word}' in {filepath}"

        elif op == "char_count":
            with open(filepath, 'r') as f:
                content = f.read()
            return f" Character Count in {filepath}: {len(content)}"

        elif op == "line_count":
            with open(filepath, 'r') as f:
                lines = f.readlines()
            return f" Line Count in {filepath}: {len(lines)}"

        elif op == "freq_words":
            with open(filepath, 'r') as f:
                words = f.read().split()
            freq = Counter(words)
            top_5 = freq.most_common(5)
            return f" Top 5 Frequent Words in {filepath}: {top_5}"

        elif op == "sort":
            with open(filepath, 'r') as f:
                lines = f.readlines()
            lines_sorted = sorted(lines)
            with open(filepath, 'w') as f:
                f.writelines(lines_sorted)
            return f" Sorted file '{filepath}' alphabetically"

        elif op == "stats":
            with open(filepath, 'r') as f:
                numbers = [float(x) for x in f.read().split()]
            s = sum(numbers)
            avg = s / len(numbers)
            mn = min(numbers)
            mx = max(numbers)
            return f" Stats for {filepath}: Sum={s}, Avg={avg:.2f}, Min={mn}, Max={mx}"

        else:
            return " Unknown operation"

    except Exception as e:
        return f" Error: {e}"

# ---------------- Server Logic ----------------
clients = {}  # client_socket:username

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode()
        clients[client_socket] = username
        client_socket.send(f"Welcome {username}! Server is ready.\n".encode())

        while True:
            data = client_socket.recv(4096).decode()
            if not data:
                break
            # Perform the operation on server
            result = perform_operation(data)
            client_socket.send(result.encode())

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        username = clients.get(client_socket, "Unknown")
        print(f"[-] {username} disconnected.")
        client_socket.close()
        clients.pop(client_socket, None)

def start_server():
    host = "127.0.0.1"
    port = 5000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[SERVER] Listening on {host}:{port}")

    while True:
        client_sock, _ = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    start_server()
