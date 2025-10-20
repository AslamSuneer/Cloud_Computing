import socket
import datetime

def start_udp_server():
    host = '127.1.1.1'
    port = 59781

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"[SERVER STARTED] Listening on {host}:{port}...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode().strip().lower()  # Normalize input

        if message == 'q':
            print(f"Client at {addr} disconnected.")
            continue

        print(f"Received from {addr}: {message}")

        # ---- Command responses ----
        if message == 'hello':
            reply = "Hello Client! How can I help you?"
        elif message == 'date':
            reply = f"Today's date is {datetime.date.today()}"
        elif message == 'time':
            reply = f"Current time is {datetime.datetime.now().strftime('%H:%M:%S')}"
        elif message == 'bye':
            reply = "Goodbye! Have a nice day!"
        elif message == 'help':
            reply = "Commands: hello | date | time | bye | q"
        else:
            reply = "Invalid command. Type 'help' for available commands."

        server_socket.sendto(reply.encode(), addr)

if __name__ == "__main__":
    start_udp_server()
