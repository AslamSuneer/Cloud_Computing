from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, col

# Step 1: Create SparkSession
spark = SparkSession.builder.appName("DistinctWordCountDF").getOrCreate()

# Step 2: Read text file into a DataFrame
df = spark.read.text("input.txt")  # 'value' column contains each line

# Step 3: Split lines into words, flatten, and normalize to lowercase
words_df = df.withColumn('word', explode(split(col('value'), ' ')))
words_df = words_df.withColumn('word', lower(col('word')))

# Step 4: Get distinct words
distinct_words_df = words_df.select('word').distinct()

# Step 5: Count distinct words
distinct_count = distinct_words_df.count()
print("Number of distinct words:", distinct_count)

# Optional: Show all distinct words
distinct_words_df.show(truncate=False)

# Stop SparkSession
spark.stop()
