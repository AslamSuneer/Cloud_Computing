from pyspark.sql import SparkSession

def is_palindrome(word):
    word = word.lower()
    return word == word[::-1] and len(word) > 1

# Initialize Spark
spark = SparkSession.builder.appName("PalindromeCheck").getOrCreate()

# Path to text file (update with your file path)
file_path = "input.txt"

# Read the text file into RDD
rdd = spark.sparkContext.textFile(file_path)

# Split into words
words_rdd = rdd.flatMap(lambda line: line.split())

# Filter palindrome words
palindromes_rdd = words_rdd.filter(is_palindrome)

# Get distinct palindromes and count
palindromes = palindromes_rdd.distinct().collect()
count = len(palindromes)

print("Palindrome Words Found:")
for p in palindromes:
    print(p)

print(f"\nTotal Palindromes: {count}")

spark.stop()
