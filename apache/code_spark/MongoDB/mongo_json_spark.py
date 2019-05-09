import pandas as pd
import matplotlib.pyplot as plt
import csv
import csv
from pymongo import MongoClient
conn=MongoClient('192.168.3.7',27017)
db=conn.health_20180305
u=db.user
m=u.find()


m.to_json('t.json')


conf=SparkConf().setMaster("local[*]").setAppName("recommaned")
sc=SparkContext(conf=conf)
spark=SQLContext(sc)