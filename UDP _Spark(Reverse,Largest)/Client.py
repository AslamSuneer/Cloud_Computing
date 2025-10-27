import socket

def start_udp_client():
    host = "127.0.0.1"
    port = 5001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("✅ Connected to UDP Server")
    print("Type a message to send (or 'exit' to quit)\n")

    while True:
        msg = input("Enter message: ")
        if msg.lower() == "exit":
            print("Client disconnected.")
            break

        # Send to server
        client_socket.sendto(msg.encode(), (host, port))

        # Receive response
        data, _ = client_socket.recvfrom(2048)
        print("\n--- Server Response ---")
        print(data.decode())
        print("-----------------------\n")

    client_socket.close()

if __name__ == "__main__":
    start_udp_client()
