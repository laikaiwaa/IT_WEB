from pyspark.mllib.linalg.distributed import  CoordinateMatrix,MatrixEntry,RowMatrix,IndexedRowMatrix
from pyspark import SQLContext,SparkConf,SparkContext

conf=SparkConf().setMaster("local[*]").setAppName("recommaned")
sc=SparkContext(conf=conf)
spark=SQLContext(sc)

source = spark.read.json("/hadoop/file/job/recommend/recommend_matrix.json")
rddd=source.rdd
t=RowMatrix(rddd)
t.rows.foreach(print)
RowMatrix