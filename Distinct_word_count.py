from pyspark.sql import SparkSession

# Step 1: Initialize Spark session
spark = SparkSession.builder.appName("DistinctWordCount").getOrCreate()

# Step 2: Read text file into RDD
lines = spark.sparkContext.textFile("input.txt")

# Step 3: Split lines into words
words = lines.flatMap(lambda line: line.split(" "))

# Step 4: Normalize case
words = words.map(lambda word: word.lower())

# Step 5: Remove duplicates
unique_words = words.distinct()

# Step 6: Count unique words
distinct_count = unique_words.count()

# Step 7: Display the result
print("Number of distinct words:", distinct_count)

# Optional: Show all unique words
print("Distinct words:", unique_words.collect())

spark.stop()
