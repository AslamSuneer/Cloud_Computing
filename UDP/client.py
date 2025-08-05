import socket

def start_udp_client():
    server_host = '127.1.1.1'
    server_port = 59781

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        message = input("Enter message for server: ")
        client_socket.sendto(message.encode(), (server_host, server_port))

        if message.upper() == 'Q':
            print("Client Disconnected...")
            break

        data, _ = client_socket.recvfrom(1024)
        print(f"Message from Server: {data.decode()}")

    client_socket.close()

if __name__ == "__main__":
    start_udp_client()

