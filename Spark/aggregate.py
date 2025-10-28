from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max as spark_max, min as spark_min, sum as spark_sum

# --------------------------------------
# Initialize Spark Session
# --------------------------------------
spark = SparkSession.builder.appName("TextFile_Stats_Calculator").getOrCreate()

try:
    print("\n Processing 'numbers.txt'...\n")

    # Read text file (one number per line)
    df_txt = spark.read.text("numbers.txt")

    # Convert text to numeric column
    df_txt = df_txt.withColumn("number", df_txt["value"].cast("float")).drop("value")

    # Compute Sum, Average, Minimum, Maximum
    result_txt = df_txt.agg(
        spark_sum("number").alias("Sum"),
        avg("number").alias("Average"),
        spark_min("number").alias("Minimum"),
        spark_max("number").alias("Maximum")
    )

    print("---- Results from numbers.txt ----")
    result_txt.show()

except Exception as e:
    print(f" Error while processing TXT file: {e}")

# Stop Spark Session
spark.stop()



----------------------------------------------------------------------------------------------------

CSV:

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max as spark_max, min as spark_min, sum as spark_sum

# --------------------------------------
# Initialize Spark Session
# --------------------------------------
spark = SparkSession.builder.appName("CSV_Stats_Calculator").getOrCreate()

try:
    print("\n Processing 'numbers.csv'...\n")

    # Read CSV file (with header)
    df_csv = spark.read.csv("numbers.csv", header=True, inferSchema=True)

    # Compute Sum, Average, Minimum, Maximum
    result_csv = df_csv.agg(
        spark_sum("value").alias("Sum"),
        avg("value").alias("Average"),
        spark_min("value").alias("Minimum"),
        spark_max("value").alias("Maximum")
    )

    print("---- Results from numbers.csv ----")
    result_csv.show()

except Exception as e:
    print(f" Error while processing CSV file: {e}")

# Stop Spark
spark.stop()

