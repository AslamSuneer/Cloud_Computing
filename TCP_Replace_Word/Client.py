import socket

def start_client():
    host = '127.0.0.1'
    port = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("[CONNECTED TO SERVER]\n")

    while True:
        print("Type 'exit' to close connection.\n")
        sentence = input("Enter a sentence: ").strip()
        if sentence.lower() == "exit":
            client.send("exit".encode())
            break

        old_word = input("Word to replace: ").strip()
        new_word = input("Replacement word: ").strip()

        message = f"{sentence}||{old_word}||{new_word}"
        client.send(message.encode())

        response = client.recv(1024).decode()
        print("\n[SERVER REPLY]:", response, "\n")

    client.close()


if __name__ == "__main__":
    start_client()
