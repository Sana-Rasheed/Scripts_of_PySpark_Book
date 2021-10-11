# -*- coding: utf-8 -*-
"""JSON Functions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I1xAAe8zAO2i14H-DRPQNF4N26q39doc
"""

from pyspark.sql import SparkSession,Row
spark = SparkSession.builder.appName('Spark').getOrCreate()

jsonString="""{"Zipcode":704,"ZipCodeType":"STANDARD","City":"PARC PARQUE","State":"PR"}"""
df=spark.createDataFrame([(1, jsonString)],["id","value"])
df.show(truncate=False)

#Convert JSON string column to Map type
from pyspark.sql.types import MapType,StringType
from pyspark.sql.functions import from_json
df2=df.withColumn("value",from_json(df.value,MapType(StringType(),StringType())))
df2.printSchema()
df2.show(truncate=False)

from pyspark.sql.functions import to_json,col
df2.withColumn("value",to_json(col("value"))) \
   .show(truncate=False)

from pyspark.sql.functions import json_tuple
df.select(col("id"),json_tuple(col("value"),"Zipcode","ZipCodeType","City")) \
    .toDF("id","Zipcode","ZipCodeType","City") \
    .show(truncate=False)

from pyspark.sql.functions import get_json_object
df.select(col("id"),get_json_object(col("value"),"$.ZipCodeType").alias("ZipCodeType")) \
    .show(truncate=False)

from pyspark.sql.functions import schema_of_json,lit
schemaStr=spark.range(1) \
    .select(schema_of_json(lit("""{"Zipcode":704,"ZipCodeType":"STANDARD","City":"PARC PARQUE","State":"PR"}"""))) \
    .collect()[0][0]
print(schemaStr)

from pyspark.sql import SparkSession,Row
spark = SparkSession.builder.appName('Spark').getOrCreate()

#read json from text file
dfFromTxt=spark.read.text("/FileStore/tables/zipcodes_json-1.txt")
dfFromTxt.printSchema()

# Create Schema of the JSON column
from pyspark.sql.types import StructType,StructField, StringType
schema = StructType([ 
    StructField("Zipcode",StringType(),True), 
    StructField("ZipCodeType",StringType(),True), 
    StructField("City",StringType(),True), 
    StructField("State", StringType(), True)
  ])

#Convert json column to multiple columns
from pyspark.sql.functions import col,from_json
dfJSON = dfFromTxt.withColumn("jsonData",from_json(col("value"),schema)) \
                   .select("jsonData.*")
dfJSON.printSchema()
dfJSON.show(truncate=False)

# Alternatively using select
dfFromTxt.select(from_json(col("value"), schema).alias("data")) \
         .select("data.*") \
         .show()

#read json from csv file
dfFromCSV=spark.read.option("header",True) \
               .csv("/FileStore/tables/zipcodes-3.csv")
dfFromCSV.printSchema()
dfFromCSV.show(truncate=False)

#Read json from string
data= [(""" {"Zipcode":704,"ZipCodeType":"STANDARD","City":"PARC PARQUE","State":"PR"} """)]
rdd = spark.sparkContext.parallelize(data)
df2 = spark.read.json(rdd)
df2.show()
