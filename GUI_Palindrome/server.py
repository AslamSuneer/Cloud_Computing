import socket
import threading
from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder \
    .appName("PalindromeServer") \
    .master("local[*]") \
    .getOrCreate()

clients = {}  # client_socket: username

def find_palindromes(text):
    """Use PySpark to find palindrome words in text"""
    sc = spark.sparkContext
    words = text.split()
    rdd = sc.parallelize(words)
    pal_rdd = rdd.filter(lambda w: w.lower() == w.lower()[::-1])
    pal_list = pal_rdd.collect()
    return pal_list, len(pal_list)

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(4096).decode()
            if not data:
                break

            # Find palindromes using Spark
            pal_list, count = find_palindromes(data)
            response = f"Palindromes: {pal_list}\nCount: {count}"
            client_socket.send(response.encode())

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()

def start_server():
    host = "127.0.0.1"
    port = 6000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[SERVER STARTED] Listening on {host}:{port}")

    while True:
        client_sock, addr = server.accept()
        print(f"[+] Client connected: {addr}")
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    start_server()
