from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder.appName("LongestShortestWordCount").getOrCreate()
sc = spark.sparkContext

# Input text file
file_path = "words.txt"   # <-- make sure to have this text file

# Read file and split into words
text_rdd = sc.textFile(file_path)
words_rdd = text_rdd.flatMap(lambda line: line.split()).filter(lambda w: w.isalpha())

# Map each word to its length
word_lengths = words_rdd.map(lambda w: (w, len(w)))

# Find maximum and minimum word lengths
max_len = word_lengths.map(lambda x: x[1]).max()
min_len = word_lengths.map(lambda x: x[1]).min()

# Filter words matching those lengths
longest_words = word_lengths.filter(lambda x: x[1] == max_len).map(lambda x: x[0]).distinct().collect()
shortest_words = word_lengths.filter(lambda x: x[1] == min_len).map(lambda x: x[0]).distinct().collect()

# Count them
longest_count = len(longest_words)
shortest_count = len(shortest_words)

# Display results
print(" Longest Words (length =", max_len, "):", ", ".join(longest_words))
print(" Count of Longest Words:", longest_count)
print(" Shortest Words (length =", min_len, "):", ", ".join(shortest_words))
print(" Count of Shortest Words:", shortest_count)

spark.stop()
