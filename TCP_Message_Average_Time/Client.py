import socket
import time

def start_client():
    host = '127.0.0.1'
    port = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("[CONNECTED TO SERVER]\n")

    total_time = 0
    num_messages = 10

    for i in range(1, num_messages + 1):
        msg = input(f"Enter message {i}: ").strip()
        if not msg:
            print(" Empty message skipped.")
            continue

        # Measure round-trip time
        start_time = time.time()
        client.send(msg.encode())
        reply = client.recv(1024).decode()
        end_time = time.time()

        rtt = (end_time - start_time) * 1000  # ms
        total_time += rtt

        print(f"Server Reply: {reply}")
        print(f" Round Trip Time: {rtt:.3f} ms\n")

    avg_rtt = total_time / num_messages
    print(f" Average Round Trip Time for 10 messages: {avg_rtt:.3f} ms")

    client.close()
    print("[DISCONNECTED FROM SERVER]")

if __name__ == "__main__":
    start_client()
