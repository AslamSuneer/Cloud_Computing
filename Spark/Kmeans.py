from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler

# --------------------------------------
# Initialize Spark Session
# --------------------------------------
spark = SparkSession.builder.appName("KMeans_File_Input").getOrCreate()

# --------------------------------------
#  Read Data from File
# --------------------------------------
# You can use either 'points.csv' or 'points.txt'
# Format example (CSV):
# id,x,y
# 0,1.0,2.0
# 1,1.5,1.8
# 2,5.0,8.0
# 3,8.0,8.0
# 4,1.2,0.8
# 5,9.0,11.0

try:
    file_path = "points.csv"   # <-- change to your file path if needed

    print(f"\n Reading data from: {file_path}\n")
    df = spark.read.csv(file_path, header=True, inferSchema=True)

    print(" Input Data:")
    df.show()

except Exception as e:
    print(f" Error reading file: {e}")
    spark.stop()
    exit()

# --------------------------------------
#  Combine 'x' and 'y' into a feature vector
# --------------------------------------
assembler = VectorAssembler(inputCols=["x", "y"], outputCol="features")
df_features = assembler.transform(df)

print(" Data after adding feature vector:")
df_features.show()

# --------------------------------------
#  Apply K-Means clustering
# --------------------------------------
kmeans = KMeans(k=2, seed=1)   # Set k = number of clusters
model = kmeans.fit(df_features)

# --------------------------------------
#  Predict cluster for each point
# --------------------------------------
predictions = model.transform(df_features)

print(" Cluster Predictions:")
predictions.select("id", "x", "y", "prediction").show()

# --------------------------------------
#  Display cluster centers
# --------------------------------------
centers = model.clusterCenters()
print("📍 Cluster Centers:")
for i, center in enumerate(centers):
    print(f"Cluster {i}: {center}")

# --------------------------------------
#  Evaluate clustering (WCSS)
# --------------------------------------
wcss = model.summary.trainingCost
print(f"\n Within Set Sum of Squared Errors (WCSS): {wcss}")

# --------------------------------------
# Stop Spark Session
# --------------------------------------
spark.stop()
