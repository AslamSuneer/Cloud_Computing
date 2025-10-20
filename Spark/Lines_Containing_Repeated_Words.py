from pyspark.sql import SparkSession
from pyspark.sql.functions import split, size, array_distinct, col

# Step 1: Create SparkSession
spark = SparkSession.builder.appName("LinesWithRepeatedWords").getOrCreate()

# Step 2: Read text file into DataFrame
df = spark.read.text("input.txt")  # 'value' column contains each line

# Step 3: Split each line into words
df_words = df.withColumn("words", split(col("value"), " "))

# Step 4: Count words and count distinct words
df_words = df_words.withColumn("word_count", size(col("words"))) \
                   .withColumn("distinct_count", size(array_distinct(col("words"))))

# Step 5: Filter lines where word_count > distinct_count (i.e., repeated words)
lines_with_repeats = df_words.filter(col("word_count") > col("distinct_count"))

# Step 6: Show the lines with repeated words
lines_with_repeats.select("value").show(truncate=False)

# Step 7: Count the number of such lines
repeat_line_count = lines_with_repeats.count()
print("Number of lines with repeated words:", repeat_line_count)

spark.stop()
