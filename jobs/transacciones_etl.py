import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import concat_ws, col

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

df = glueContext.create_dynamic_frame.from_catalog(
    database="datalake-db",
    table_name="transacciones"
).toDF()

# Crear columna fecha concatenando
df = df.withColumn("Fecha", concat_ws("/", col("year"), col("month"), col("day")))

df.coalesce(1).write.mode("overwrite").parquet("s3://datalake-stage-bucket-pragma-prueba-btg/transacciones/")
job.commit()