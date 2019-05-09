from pyspark import SparkConf, SparkContext,SQLContext
from pyspark.sql import HiveContext
import os
path=os.getcwd()

conf=SparkConf().setMaster("local[*]").setAppName("linkhive")
sc=SparkContext(conf=conf)
spark=SQLContext(sc)
hive = HiveContext(sc)

# 讀取hive數據
show=hive.sql("show databases")
show.show()
show=hive.sql("use hive_mysql")
show=hive.sql("show tables")
show.show()
show=hive.sql("select _id from hive_table")
print('thetypefromhive',type(show))
show.show()

#保存hive數據

file=path+"/di.json"
js=hive.read.json(file)


# js.write.mode(saveMode="overwrite").saveAsTable("hive_mysql.hive_table")




