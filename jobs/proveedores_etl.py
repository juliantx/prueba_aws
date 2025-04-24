import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import upper

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


df = glueContext.create_dynamic_frame.from_catalog(
    database="datalake-db",
    table_name="proveedores"
).toDF()

# Convertir columna a mayúsculas
df = df.withColumn("nombre_proveedor", upper(df["nombre_proveedor"]))

# Guardar
df.write.mode("overwrite").parquet("s3://datalake-stage-bucket-pragma-prueba-btg/proveedores/")
job.commit()