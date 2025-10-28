import socket
import time

def start_udp_server():
    host = '127.0.0.1'
    port = 5000

    # UDP socket (SOCK_DGRAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    print(f"[SERVER STARTED] Listening on {host}:{port}")

    message_times = {}  # To store message timestamps for average (optional if client calculates)

    count = 0
    while True:
        data, addr = server.recvfrom(1024)
        message = data.decode()

        if message.lower() == "exit":
            print(f"[DISCONNECTED] Client {addr} closed the connection.")
            break

        count += 1
        print(f"[RECEIVED] From {addr}: {message}")

        # Reply to client
        reply = f"Server received your message: '{message}'"
        server.sendto(reply.encode(), addr)

    server.close()

if __name__ == "__main__":
    start_udp_server()
