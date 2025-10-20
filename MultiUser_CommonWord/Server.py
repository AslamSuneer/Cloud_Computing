import socket
import threading

clients = {}  # client_socket:username
last_messages = {}  # client_socket:last_message

# ----------------------- Optional Client Limit -----------------------
# MAX_CLIENTS = 2  # Uncomment to limit number of clients

def broadcast(message, sender_socket=None):
    for client_sock in clients:
        if client_sock != sender_socket:
            try:
                client_sock.send(message.encode())
            except:
                client_sock.close()

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode()
        clients[client_socket] = username
        last_messages[client_socket] = ""
        broadcast(f"{username} has joined the chat.", client_socket)
        print(f"[+] {username} connected.")

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Update last message
            last_messages[client_socket] = message

            # Find common words with other clients
            common_words_set = set(message.lower().split())
            for other_sock, other_msg in last_messages.items():
                if other_sock != client_socket:
                    other_words_set = set(other_msg.lower().split())
                    common = common_words_set.intersection(other_words_set)
                    if common:
                        broadcast(f"[COMMON WORDS] {username}: {', '.join(common)}")

            # Broadcast the original message
            broadcast(f"{username}: {message}", client_socket)

    except:
        pass
    finally:
        username = clients.get(client_socket, "Unknown")
        print(f"[-] {username} disconnected.")
        broadcast(f"{username} has left the chat.", client_socket)
        client_socket.close()
        clients.pop(client_socket, None)
        last_messages.pop(client_socket, None)

def start_server():
    host = '127.0.0.1'
    port = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"[SERVER STARTED] Listening on {host}:{port}")

    while True:
        client_sock, addr = server.accept()

        # ---------------- Optional Client Limit Check ----------------
        # Uncomment the following block to limit clients to MAX_CLIENTS
        # if 'MAX_CLIENTS' in globals() and len(clients) >= MAX_CLIENTS:
        #     client_sock.send("Server full. Only 2 clients allowed.".encode())
        #     client_sock.close()
        #     print(f"[REJECTED] Connection from {addr} - Server full")
        #     continue

        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    start_server()
