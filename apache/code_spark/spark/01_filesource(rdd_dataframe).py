from pyspark import SparkContext,SQLContext,SparkConf
import os
path=os.getcwd()
# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3.5"

conf=SparkConf().setMaster("local[*]").setAppName("recommaned")
# conf=SparkConf().setMaster("spark://10.26.11.234:7077").setAppName("linkhive")
sc=SparkContext(conf=conf)
sqlContext = SQLContext(sc)

# 讀取TXT文本，rdd
txtfile=sc.textFile(path+"/log.txt")
print('textfiletype',type(txtfile))
txtfile.foreach(print)
print(txtfile.getNumPartitions())
# 保存
# txtfile.saveAsTextFile(path+"/logsave.txt")

# 讀取json,dataframe
file=path+"/di.json"
js=sqlContext.read.json(file)
print('jstype',type(js))
js.foreach(print)
everyroe=js.collect()
print(type(everyroe))

js.show(truncate=False)
js.printSchema()

js.select("_id").show()

#sql
js.registerTempTable("user")
# sall=spark.sql("slect * from user")
set = sqlContext.sql("show columns from user")
set.show()











