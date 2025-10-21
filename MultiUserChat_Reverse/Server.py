import socket
import threading

clients = {}  # Stores client_socket:username

def broadcast(message, sender_socket=None):
    """Send message to all connected clients except the sender."""
    disconnected_clients = []
    for client_sock in clients:
        try:
            client_sock.send(message.encode())
        except:
            client_sock.close()
            disconnected_clients.append(client_sock)

    for dc in disconnected_clients:
        del clients[dc]

def handle_client(client_socket):
    try:
        # Receive username from client
        username = client_socket.recv(1024).decode()
        clients[client_socket] = username
        broadcast(f"{username} has joined the chat.")
        print(f"[+] {username} connected.")

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Reverse each word in the message
            words = message.split()
            reversed_words = [word[::-1] for word in words]
            reversed_msg = " ".join(reversed_words)

            # Display in server console
            print(f"[CHAT] {username}: {message} → {reversed_msg}")

            # Broadcast original + reversed message
            broadcast(f"{username}: {message}\n→ {reversed_msg}")

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        username = clients.get(client_socket, "Unknown")
        print(f"[-] {username} disconnected.")
        broadcast(f"{username} has left the chat.")
        client_socket.close()
        if client_socket in clients:
            del clients[client_socket]

def start_server():
    host = '127.0.0.1'
    port = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[SERVER STARTED] Listening on {host}:{port}")

    while True:
        client_sock, _ = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    start_server()
