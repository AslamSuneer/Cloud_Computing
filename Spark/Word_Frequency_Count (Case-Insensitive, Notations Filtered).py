from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, regexp_replace, col

# --------------------------------
# Initialize Spark Session
# --------------------------------
spark = SparkSession.builder.appName("WordFrequencyFiltered").getOrCreate()

# --------------------------------
# Read the input text file
# --------------------------------
df = spark.read.text("input.txt")

# --------------------------------
# Clean text:
# - Remove punctuation
# - Convert to lowercase
# - Split into words
# --------------------------------
cleaned = df.select(
    explode(
        split(
            lower(regexp_replace(col("value"), r"[^a-zA-Z0-9\s]", "")),r"\s+")).alias("word"))

# Remove empty entries
cleaned = cleaned.filter(col("word") != "")

# --------------------------------
# Count frequency of each word
# --------------------------------
word_counts = cleaned.groupBy("word").count().orderBy(col("count").desc())

# --------------------------------
# Show results
# --------------------------------
print("\n===== Word Frequency (Filtered & Case-Insensitive) =====\n")
word_counts.show(truncate=False)

# --------------------------------
# Stop Spark Session
# --------------------------------
spark.stop()
