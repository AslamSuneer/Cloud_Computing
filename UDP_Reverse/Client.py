import socket

def start_udp_client():
    host = "127.0.0.1"
    port = 5001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("✅ Connected to UDP Reverse Server")
    print("Type a message (or 'exit' to quit)\n")

    while True:
        msg = input("Enter message: ")
        if msg.lower() == "exit":
            print("Client disconnected.")
            break

        client_socket.sendto(msg.encode(), (host, port))
        data, _ = client_socket.recvfrom(1024)
        print(f"Server Reversed: {data.decode()}\n")

    client_socket.close()

if __name__ == "__main__":
    start_udp_client()
