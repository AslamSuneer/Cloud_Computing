import socket
import threading

clients = {}  # Stores client_socket:username

def broadcast(message, sender_socket=None):
    """Send message to all clients except the sender."""
    for client_sock in clients:
        if client_sock != sender_socket:
            try:
                client_sock.send(message.encode())
            except:
                client_sock.close()

def handle_client(client_socket):
    try:
        # Receive username
        username = client_socket.recv(1024).decode()
        clients[client_socket] = username
        broadcast(f"{username} has joined the chat.", client_socket)
        print(f"[+] {username} connected.")

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            broadcast(f"{username}: {message}", client_socket)
    except:
        pass
    finally:
        username = clients.get(client_socket, "Unknown")
        print(f"[-] {username} disconnected.")
        broadcast(f"{username} has left the chat.", client_socket)
        client_socket.close()
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
