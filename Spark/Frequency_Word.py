# Example: most frequent words
word_counts = df.groupBy("word").count()
word_counts.orderBy(col("count").desc()).show(5)  # Top 5 frequent words
