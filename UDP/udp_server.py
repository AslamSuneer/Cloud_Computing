import socket

def start_udp_server():
    host = '127.1.1.1'
    port = 59781

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"UDP Server Listening on {host}:{port}...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()

        if message.upper() == 'Q':
            print(f"Client at {addr} disconnected.")
            continue  

        print(f"Received from {addr}: {message}")
        reply = input("Reply to client: ")
        server_socket.sendto(reply.encode(), addr)

    server_socket.close()

if __name__ == "__main__":
    start_udp_server()

