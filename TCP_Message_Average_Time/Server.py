import socket

def start_server():
    host = '127.0.0.1'
    port = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"[SERVER STARTED] Listening on {host}:{port}")

    conn, addr = server.accept()
    print(f"[CONNECTED] Client: {addr}")

    count = 0
    while count < 10:
        data = conn.recv(1024).decode()
        if not data:
            break

        print(f"[MESSAGE RECEIVED] {data}")
        reply = f"Message received: '{data}'"
        conn.send(reply.encode())
        count += 1

    print(f"[INFO] 10 messages processed. Closing connection.")
    conn.close()
    server.close()
    print("[SERVER CLOSED]")

if __name__ == "__main__":
    start_server()
