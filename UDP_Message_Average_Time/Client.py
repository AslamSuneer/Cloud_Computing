import socket
import time

def start_udp_client():
    host = '127.0.0.1'
    port = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rtt_list = []

    print("\nType 10 messages (press Enter after each):\n")

    for i in range(1, 11):  # Send 10 messages
        msg = input(f"Message {i}: ").strip()
        if not msg:
            print(" Empty message skipped.")
            continue

        start_time = time.time()
        client.sendto(msg.encode(), (host, port))
        data, _ = client.recvfrom(1024)
        end_time = time.time()

        rtt = (end_time - start_time) * 1000  # in ms
        rtt_list.append(rtt)

        print(f"Server Reply: {data.decode()}")
        print(f"Round Trip Time (RTT): {rtt:.3f} ms\n")

    if rtt_list:
        avg_rtt = sum(rtt_list) / len(rtt_list)
        print(f" Average Round Trip Time: {avg_rtt:.3f} ms")

    client.sendto("exit".encode(), (host, port))
    client.close()

if __name__ == "__main__":
    start_udp_client()
