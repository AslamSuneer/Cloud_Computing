import socket
from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder.appName("LongestShortestWords").getOrCreate()
sc = spark.sparkContext

def process_message(message):
    words = [w for w in message.split() if w.isalpha()]
    if not words:
        return "No valid words found."

    # Parallelize words using Spark
    rdd = sc.parallelize(words)

    # Compute length of each word
    word_lengths = rdd.map(lambda w: (w, len(w)))

    # Find min and max length
    max_len = word_lengths.map(lambda x: x[1]).max()
    min_len = word_lengths.map(lambda x: x[1]).min()

    # Get all words matching longest and shortest lengths
    longest_words = word_lengths.filter(lambda x: x[1] == max_len).map(lambda x: x[0]).collect()
    shortest_words = word_lengths.filter(lambda x: x[1] == min_len).map(lambda x: x[0]).collect()

    return f"Longest words ({max_len}): {', '.join(longest_words)} | Shortest words ({min_len}): {', '.join(shortest_words)}"

def start_udp_server():
    host = "127.0.0.1"
    port = 5001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"[SERVER STARTED] Listening on {host}:{port}")

    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        print(f"\n[CLIENT MESSAGE] {message}")

        # Reverse the message
        reversed_msg = message[::-1]
        print(f"[REVERSED] {reversed_msg}")

        # Spark processing
        result = process_message(message)
        print(f"[SPARK RESULT] {result}")

        # Send reversed + spark result
        final_response = f"Reversed: {reversed_msg}\n{result}"
        server_socket.sendto(final_response.encode(), addr)

if __name__ == "__main__":
    start_udp_server()
