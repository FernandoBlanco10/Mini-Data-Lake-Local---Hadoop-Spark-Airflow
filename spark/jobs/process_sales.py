import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

parser = argparse.ArgumentParser()
parser.add_argument("--input_path", required=True)
parser.add_argument("--output_path", required=True)
args = parser.parse_args()

spark = SparkSession.builder \
    .appName("ProcessSales") \
    .getOrCreate()

df = spark.read.csv(
    args.input_path,
    header=True,
    inferSchema=True
)

df = df.withColumn(
    "venta_total",
    col("precio") * col("cantidad")
)

df.show()

df.write.mode("overwrite").csv(args.output_path, header=True)

df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/datawarehouse") \
    .option("dbtable", "sales_processed") \
    .option("user", "admin") \
    .option("password", "fblanco123") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

spark.stop()
