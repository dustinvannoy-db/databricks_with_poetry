from pyspark.sql import functions as fn
import pyspark_functions
import os

spark = pyspark_functions.prepare_spark()
df = pyspark_functions.create_sample_dataframe(spark)
updated_df = df.withColumn("created_date", fn.current_date())
updated_df.show()
print("done")