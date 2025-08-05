import socket

def start_server():
    host = '127.1.0.1'
    port = 65446

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"TCP Server Connecting on {host}:{port}...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print("Client disconnected.")
                break
            print("Client says:", data.decode())

            reply = input("Enter reply to Client: ")
            conn.sendall(reply.encode())
        except ConnectionResetError:
            print("Client closed the connection.")
            break

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()

