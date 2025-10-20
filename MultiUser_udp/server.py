import socket
import threading

# Store clients as {address: username}
clients = {}

def broadcast(message, sender_addr=None, server_socket=None):
    for addr in clients:
        if addr != sender_addr:
            try:
                server_socket.sendto(message.encode(), addr)
            except:
                pass  # Ignore if sending fails

def start_server():
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"[UDP SERVER STARTED] Listening on {host}:{port}")

    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            message = data.decode()

            # New client sends their username first
            if addr not in clients:
                clients[addr] = message
                broadcast(f"{message} has joined the chat.", sender_addr=addr, server_socket=server_socket)
                print(f"[+] {message} connected from {addr}")
            else:
                username = clients[addr]
                broadcast(f"{username}: {message}", sender_addr=addr, server_socket=server_socket)
                print(f"[{username}] {message}")
        except KeyboardInterrupt:
            print("Server stopped manually.")
            break

    server_socket.close()

if __name__ == "__main__":
    start_server()
