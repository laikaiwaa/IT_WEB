from pyspark import SparkConf, SparkContext,SQLContext
from pyspark.sql import HiveContext
import json
import os
path=os.getcwd()

conf=SparkConf().setMaster("local[*]").setAppName("linkhive")
sc=SparkContext(conf=conf)
spark=SQLContext(sc)


host = '192.168.159.100'
table = 'forsparkread'
conf = {"hbase.zookeeper.quorum": host, "hbase.mapreduce.inputtable": table}
keyConv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"
valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"

rdd = sc.newAPIHadoopRDD("org.apache.hadoop.hbase.mapreduce.TableInputFormat",
                         "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
                         "org.apache.hadoop.hbase.client.Result",
                         keyConverter=keyConv,valueConverter=valueConv,conf=conf)
#
# df = spark.read.format('org.apache.spark.sql.execution.datasources.hbase') \
#     .option('hbase.table','forsparkread')\
#     .option('hbase.columns.mapping',
#             'a int :a,'
#             'b STRING info:b,'
#             'year STRING info:year,'
#             'views STRING analytics:views').load()

rdd.show()