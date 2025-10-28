from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split

# --------------------------------
# Initialize Spark Session
# --------------------------------
spark = SparkSession.builder.appName("MostFrequentWords").getOrCreate()

# --------------------------------
# Read text file
# --------------------------------
df = spark.read.text("words.txt")

# Split lines into individual words
words_df = df.select(explode(split(col("value"), "\\s+")).alias("word"))

# Remove empty strings
words_df = words_df.filter(col("word") != "")

# --------------------------------
# Count occurrences of each word
# --------------------------------
word_counts = words_df.groupBy("word").count()

# --------------------------------
# Sort by frequency (descending)
# --------------------------------
top_words = word_counts.orderBy(col("count").desc())

# Show top 5 most frequent words
print("\n---- Top 5 Most Frequent Words ----")
top_words.show(5)

# --------------------------------
# Stop Spark Session
# --------------------------------
spark.stop()
