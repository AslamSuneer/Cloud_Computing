# Example CSV: numbers.csv
# value
# 10
# 20
# 30

df = spark.read.csv("numbers.csv", header=True, inferSchema=True)
df.agg({"value": "sum"}).show()     # Sum
df.agg({"value": "avg"}).show()     # Average
df.agg({"value": "min"}).show()     # Minimum
df.agg({"value": "max"}).show()     # Maximum
