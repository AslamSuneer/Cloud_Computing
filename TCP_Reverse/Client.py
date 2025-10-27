import socket

def start_client():
    host = "127.0.0.1"
    port = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("[CONNECTED] Type messages to send to the server. Type 'exit' to quit.\n")

    while True:
        msg = input("You: ")
        if msg.lower() == 'exit':
            print("Disconnected from server.")
            break

        client.send(msg.encode())
        data = client.recv(1024).decode()
        print(f"Server (Reversed): {data}")

    client.close()

if __name__ == "__main__":
    start_client()
