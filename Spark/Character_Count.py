from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col

spark = SparkSession.builder.appName("CharacterCount").getOrCreate()

df = spark.read.text("input.txt")

# Split each line into characters
chars_df = df.withColumn("char", explode(split(col("value"), "")))
char_counts = chars_df.groupBy("char").count()

char_counts.show(truncate=False)
spark.stop()
