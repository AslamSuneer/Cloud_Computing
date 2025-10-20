from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, col

# Step 1: Create SparkSession
spark = SparkSession.builder.appName("WordCountDF").getOrCreate()

# Step 2: Read text file into a DataFrame
df = spark.read.text("input.txt")  # 'value' column contains each line

# Step 3: Split lines into words, flatten, and normalize to lowercase
words_df = df.withColumn('word', explode(split(col('value'), ' ')))
words_df = words_df.withColumn('word', lower(col('word')))

# Step 4: Count occurrences of each word
word_counts_df = words_df.groupBy('word').count()

# Step 5: Show the results
word_counts_df.show(truncate=False)

# Stop SparkSession
spark.stop()
