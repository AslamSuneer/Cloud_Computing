from pyspark.sql import SparkSession

# -----------------------------
# Initialize Spark Session
# -----------------------------
spark = SparkSession.builder.appName("JoinFromTextFiles").getOrCreate()

# -----------------------------
# Read students.txt
# -----------------------------
students = spark.read.option("header", "false").option("inferSchema", "true").csv("students.txt")
students = students.withColumnRenamed("_c0", "id").withColumnRenamed("_c1", "name")

# -----------------------------
# Read scores.txt
# -----------------------------
scores = spark.read.option("header", "false").option("inferSchema", "true").csv("scores.txt")
scores = scores.withColumnRenamed("_c0", "id").withColumnRenamed("_c1", "score")

# -----------------------------
# Perform INNER JOIN on 'id'
# -----------------------------
joined = students.join(scores, on="id", how="inner")

print("\n---- Joined Data ----")
joined.show()

# -----------------------------
# Stop Spark
# -----------------------------
spark.stop()




students.txt:
1,Alice
2,Bob
3,Charlie

scores.txt:
1,90
2,85
3,95
