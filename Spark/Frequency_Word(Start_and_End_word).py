from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower, regexp_replace

# --------------------------------
# Initialize Spark Session
# --------------------------------
spark = SparkSession.builder.appName("WordsStartingEnding").getOrCreate()

# --------------------------------
# Read text file
# --------------------------------
df = spark.read.text("words.txt")

# --------------------------------
# Clean and preprocess text
# --------------------------------
# - Convert to lowercase
# - Remove punctuation/special characters
# - Split by whitespace into words
cleaned_df = df.select(
    explode(
        split(
            lower(
                regexp_replace(col("value"), r"[^a-zA-Z\s]", "")
            ),
            r"\s+"
        )
    ).alias("word")
)

# Remove any empty words
cleaned_df = cleaned_df.filter(col("word") != "")

# --------------------------------
# Filter words that start with 'a' and end with 'm'
# --------------------------------
filtered_words = cleaned_df.filter(col("word").rlike(r"^a.*m$"))

# --------------------------------
# Count occurrences of each filtered word
# --------------------------------
word_counts = filtered_words.groupBy("word").count()

# --------------------------------
# Sort by frequency (descending)
# --------------------------------
sorted_counts = word_counts.orderBy(col("count").desc())

# --------------------------------
# Show all words that match the condition
# --------------------------------
print("\n---- Words that start with 'a' and end with 'm' ----")
sorted_counts.show(truncate=False)

# --------------------------------
# Stop Spark Session
# --------------------------------
spark.stop()
