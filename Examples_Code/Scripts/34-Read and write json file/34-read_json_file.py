# -*- coding: utf-8 -*-
"""Read JSON file.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1foyTKATeMPYFbVkxGlG-wAX493yONUsJ
"""

# Read JSON file into dataframe
df = spark.read.json("/FileStore/tables/zipcodes-1.json")
df.printSchema()

# Read JSON file into dataframe
df = spark.read.format('org.apache.spark.sql.json') \
        .load("/FileStore/tables/zipcodes-1.json")

# Read multiline json file
multiline_df = spark.read.option("multiline","true") \
      .json("/FileStore/tables/multiline_zipcode.json")
multiline_df.show()

# Read multiple files
df2 = spark.read.json(
    ['/FileStore/tables/multiline_zipcode.json','/FileStore/tables/zipcodes-1.json'])
df2.show()

# Read all JSON files from a folder
df3 = spark.read.json("/FileStore/tables/*.json")
df3.show()

from pyspark.sql.types import StructType,StructField, StringType,IntegerType,DoubleType,BooleanType
# Define custom schema
schema = StructType([
      StructField("RecordNumber",IntegerType(),True),
      StructField("Zipcode",IntegerType(),True),
      StructField("ZipCodeType",StringType(),True),
      StructField("City",StringType(),True),
      StructField("State",StringType(),True),
      StructField("LocationType",StringType(),True),
      StructField("Lat",DoubleType(),True),
      StructField("Long",DoubleType(),True),
      StructField("Xaxis",IntegerType(),True),
      StructField("Yaxis",DoubleType(),True),
      StructField("Zaxis",DoubleType(),True),
      StructField("WorldRegion",StringType(),True),
      StructField("Country",StringType(),True),
      StructField("LocationText",StringType(),True),
      StructField("Location",StringType(),True),
      StructField("Decommisioned",BooleanType(),True),
      StructField("TaxReturnsFiled",StringType(),True),
      StructField("EstimatedPopulation",IntegerType(),True),
      StructField("TotalWages",IntegerType(),True),
      StructField("Notes",StringType(),True)
  ])

df_with_schema = spark.read.schema(schema) \
        .json("/FileStore/tables/zipcodes.json")
df_with_schema.printSchema()
df_with_schema.show()

spark.sql("CREATE OR REPLACE TEMPORARY VIEW zipcode USING json OPTIONS" + 
      " (path '/FileStore/tables/zipcodes.json')")
spark.sql("select * from zipcode").show()

df2.write.json("/tmp/spark_output/zipcodes.json")

df2.write.mode('Overwrite').json("/tmp/spark_output/zipcodes.json")
