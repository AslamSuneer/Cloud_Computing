import socket
import threading

def handle_client(client_socket, addr):
    print(f"[+] Connected to {addr}")

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        print(f"[CLIENT -> SERVER] {data}")

        # Reverse the message and send back
        reversed_msg = data[::-1]
        client_socket.send(reversed_msg.encode())

    print(f"[-] Client {addr} disconnected.")
    client_socket.close()

def start_server():
    host = "127.0.0.1"
    port = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[SERVER STARTED] Listening on {host}:{port}")

    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
