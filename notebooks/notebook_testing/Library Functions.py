# Databricks notebook source
def generate_data(n=1000, name='my_cool_data'):
  df = spark.range(0, n)
  df.createOrReplaceTempView(name)

# COMMAND ----------

import random
def get_data_prediction():
  return 42 if random.random() < 0.6 else 128

# COMMAND ----------


