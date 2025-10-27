import socket

def start_udp_server():
    host = "127.0.0.1"
    port = 5001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"[UDP SERVER STARTED] Listening on {host}:{port}")

    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        print(f"[CLIENT MESSAGE] {message}")

        # Reverse message
        reversed_msg = message[::-1]
        print(f"[REVERSED] {reversed_msg}")

        server_socket.sendto(reversed_msg.encode(), addr)

if __name__ == "__main__":
    start_udp_server()
