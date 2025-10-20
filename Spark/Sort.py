df.orderBy(col("value").desc()).show()  # Descending sort
df.orderBy(col("value").asc()).show()   # Ascending sort
