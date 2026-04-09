from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("ProcessSales") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()

df = spark.read.csv(
    "/opt/spark/data/sales.csv",
    header=True,
    inferSchema=True
)

df = df.withColumn(
    "venta_total",
    col("precio") * col("cantidad")
)

df.show()

df.write.mode("overwrite").csv(
    "/opt/spark/output/sales_processed",
    header=True
)

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