import os
os.environ["PYSPARK_PYTHON"]="/usr/bin/python3.5"
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql import HiveContext
import pandas as pd
conf=SparkConf().setMaster("local[*]").setAppName("recommaned")
sc=SparkContext(conf=conf)

spark=SQLContext(sc)
file="資治通鑒.txt"
js=sc.textFile(file)



##single
#jp_single=js.flatMap(lambda x:x).filter(lambda x:(x!="-"and x!="、"and x!=" "and x!="，"and x!="；"
#                                                 and x!="。" and x!="：" and x!="=" and x!="“" and x!="”")).map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y)
#print(jp_single)
#jp_single.foreach(print)

#frame=spark.createDataFrame(jp_single,('資治通鑒_单字','num'))
#frame.registerTempTable('stat')

#order=spark.sql('select * from stat order by num DESC ')
#order.show()
#orderpandas=order.toPandas()
#orderpandas.to_csv('資治通鑒_单字.csv',encoding='utf-8-sig')
##single-----------------------------

jp_double=js.flatMap(lambda x:x.split("。")).flatMap(lambda x:x.split("，")).flatMap(lambda x:x.split(" "))\
    .filter(lambda x:x!="").flatMap(lambda x:{(x[i]+","+x[i+1],1) for i in range(len(x)-1)}).reduceByKey(lambda x,y:x+y)
jp_double2=jp_double.map(lambda x:(x[0].split(",")[0],x[0].split(",")[1],x[1]))
print(jp_double2)

jp_double2.foreach(print)
frame_double=spark.createDataFrame(jp_double2,("word1","word2","num"))
frame_double.registerTempTable('stat')
frame_double.printSchema()
order_double=spark.sql("select * from stat  where  num>100  order by num desc")
order_double.show(100)
orderdoublrpandas=order_double.toPandas()
orderdoublrpandas.to_csv('資治通鑒_詞語.csv',encoding='utf-8-sig')

