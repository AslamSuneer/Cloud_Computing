import socket

def start_server():
    host = '127.0.0.1'
    port = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    print(f"[SERVER STARTED] Listening on {host}:{port}...\n")

    conn, addr = server.accept()
    print(f"[CONNECTED] Client: {addr}\n")

    while True:
        data = conn.recv(1024).decode()
        if not data or data.lower() == "exit":
            print("[CLIENT DISCONNECTED]")
            break

        try:
            # Data format: sentence||old_word||new_word
            sentence, old_word, new_word = data.split("||")
            modified_sentence = sentence.replace(old_word, new_word)
            response = f" Updated Sentence: {modified_sentence}"
        except ValueError:
            response = " Invalid input format. Expected: sentence||old_word||new_word"

        conn.send(response.encode())

    conn.close()
    server.close()


if __name__ == "__main__":
    start_server()
