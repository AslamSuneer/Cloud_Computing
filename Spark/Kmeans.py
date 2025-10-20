from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler

# Sample numeric dataset
data = [(0, 1.0, 2.0), (1, 1.5, 1.8), (2, 5.0, 8.0), (3, 8.0, 8.0)]
df = spark.createDataFrame(data, ["id","x","y"])

# Combine features into a single vector
assembler = VectorAssembler(inputCols=["x","y"], outputCol="features")
df_features = assembler.transform(df)

# Apply KMeans
kmeans = KMeans(k=2, seed=1)
model = kmeans.fit(df_features)
predictions = model.transform(df_features)
predictions.show()
