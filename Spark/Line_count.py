from pyspark.sql import SparkSession

# --------------------------------
# Initialize Spark Session
# --------------------------------
spark = SparkSession.builder.appName("LineCount").getOrCreate()

# --------------------------------
# Read text file
# --------------------------------
df = spark.read.text("input.txt")

# --------------------------------
# Count total number of lines
# --------------------------------
line_count = df.count()

# --------------------------------
# Display result
# --------------------------------
print("===================================")
print(" Number of lines in the file:", line_count)
print("===================================")

# --------------------------------
# Stop Spark Session
# --------------------------------
spark.stop()
