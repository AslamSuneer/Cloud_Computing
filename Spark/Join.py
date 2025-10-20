# Example: students and scores
students = spark.createDataFrame([(1,"Alice"),(2,"Bob")], ["id","name"])
scores = spark.createDataFrame([(1,90),(2,85)], ["id","score"])

joined = students.join(scores, on="id", how="inner")
joined.show()
