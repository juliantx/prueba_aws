import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import lit

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Cargar datos desde Glue Catalog
df = glueContext.create_dynamic_frame.from_catalog(
    database="datalake-db",
    table_name="clientes"
).toDF()

# Agregar columna
df = df.withColumn("region", lit("South America"))

# Escribir en Parquet
df.write.mode("overwrite").parquet("s3://datalake-stage-bucket-pragma-prueba-btg/clientes/")

job.commit()
