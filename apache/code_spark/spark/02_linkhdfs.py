from pyspark import SparkContext,SQLContext,SparkConf
from pyspark.streaming import StreamingContext
conf=SparkConf().setMaster("local[*]").setAppName("recommaned")
sc=SparkContext(conf=conf)

## 非流式读取
# m=sc.textFile("hdfs://main:9000/filetest/text.txt")
# rdd保存为hdfs文件格式
# m.saveAsTextFile("hdfs://main:9000/filetest/testwrite/")

# print(m.collect())
# 寫入

## 流式（動態變化）读取
# 开启后再往目录写数据
ssc = StreamingContext(sc,10)
lines = ssc.textFileStream("hdfs://main:9000/filetest/sparkkafkaresultstore/")
print(lines)
lines.pprint()
ssc.start()
ssc.awaitTermination()


