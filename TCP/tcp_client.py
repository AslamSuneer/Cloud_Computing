import socket

def start_client():
    host = '127.1.0.1'
    port = 65446

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        msg = input("Enter message for server (Q to quit): ")
        if msg.upper() == "Q":
            print("Client Disconnected...")
            break
        client_socket.sendall(msg.encode())
        data = client_socket.recv(1024)
        print("Message from Server:", data.decode())

    client_socket.close()

if __name__ == "__main__":
    start_client()

