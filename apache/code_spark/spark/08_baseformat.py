from pyspark import SQLContext,SparkConf,SparkContext
from pyspark.mllib.linalg.distributed import  CoordinateMatrix,MatrixEntry,RowMatrix,IndexedRowMatrix
from pyspark.ml.linalg import Vectors,Matrices,Matrix
from pyspark.mllib.regression import LabeledPoint
from pyspark.ml.feature import VectorAssembler
import pyspark.mllib.stat as st
from pyspark.mllib.feature import StandardScaler
from pyspark.ml.stat import Correlation
import pandas  as pd
import numpy as np

conf=SparkConf().setMaster("local[*]").setAppName("recommaned")
sc=SparkContext(conf=conf)
spark=SQLContext(sc)

source = spark.read.json("D:/project/recommend_system/recommend_matrix.json")
sourcerdd=sc.textFile("D:/project/recommend_system/recommend_matrix.txt")

print(type(source))
source.foreach(print)
print(type(sourcerdd))
sourcerdd.foreach(print)

#a_rdd_to_dataframe
print('a_rdd_to_dataframe')
rdd_a=sourcerdd.map(lambda x:x.split(','))
rdd_a.foreach(print)
rdd_a_df=spark.createDataFrame(rdd_a,['user1','user2','user3','user4','user5','user6'])
rdd_a_df.foreach(print)

#2_dataframe_to_vector
print('2_dataframe_to_vector')
sourcecut=source.drop('item')
vector_a=source.rdd.map(lambda x:Vectors.dense(x))
print(type(vector_a))
vector_a.foreach(print)



#2_dataframe_to_labelpoint
print('2_dataframe_to_labelpoint')
LabeledPoint_a=source.rdd.map(lambda x:LabeledPoint(x.item,[x.user1,x.user2,x.user3,x.user4,x.user5,x.user6]))
print(type(LabeledPoint_a))
LabeledPoint_a.foreach(print)

#2_dataframe_to_matrix
print('2_dataframe_to_matrix')
matrixlocal=sourcecut.rdd.reduce(lambda x,y:x+y)
matrixlocal_a=Matrices.dense(6,6,matrixlocal)
print(type(matrixlocal_a))
print(matrixlocal_a)

#3_dataframe_to_rowmatrix
print('3_dataframe_to_rowmatrix')

rmatrix=sourcecut.rdd.map(lambda x:Vectors.dense(x).toArray())
rowmatrix=RowMatrix(rmatrix)
print(type(rowmatrix))
rowmatrix.rows.foreach(print)



#distrbutued
print('distrbutued')
corr=rowmatrix.columnSimilarities()
print(type(corr))
corr.entries.foreach(print)

corr_indexrow=corr.toIndexedRowMatrix()
corr_block=corr.toBlockMatrix()
print(type(corr_indexrow))
corr_indexrow.rows.foreach(print)
print(type(corr_block))
corr_block.blocks.foreach(print)

toloca=corr_block.toLocalMatrix()
print(type(toloca))
print(toloca)
#matrix_dot
product_a=rowmatrix.multiply(toloca)
print(type(product_a))
product_a.rows.foreach(print)

t=corr_block.multiply(corr_block)
print(t)
t.blocks.foreach(print)
