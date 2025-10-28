from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# -----------------------------
# Initialize Spark Session
# -----------------------------
spark = SparkSession.builder.appName("AlphabetSort").getOrCreate()

# -----------------------------
# Read text file (alphabets.txt)
# -----------------------------
# Example file content:
# apple
# mango
# banana
# cherry

df = spark.read.text("alphabets.txt").withColumnRenamed("value", "word")

print("\n---- Ascending Order ----")
df.orderBy(col("word").asc()).show(truncate=False)

print("\n---- Descending Order ----")
df.orderBy(col("word").desc()).show(truncate=False)

# -----------------------------
# Stop Spark
# -----------------------------
spark.stop()

---------------------------------------------------------------------------------------------------------------
Number Sorting:

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# -----------------------------
# Initialize Spark Session
# -----------------------------
spark = SparkSession.builder.appName("NumberSort").getOrCreate()

# -----------------------------
# Read text file (numbers.txt)
# -----------------------------
# Example file content:
# 10
# 5
# 25
# 3
# 15

df = spark.read.text("numbers.txt")
df = df.withColumn("value", col("value").cast("float"))

print("\n---- Ascending Order ----")
df.orderBy(col("value").asc()).show()

print("\n---- Descending Order ----")
df.orderBy(col("value").desc()).show()

# -----------------------------
# Stop Spark
# -----------------------------
spark.stop()
