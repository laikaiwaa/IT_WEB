from pykafka import KafkaClient,SimpleConsumer
from pyspark import SparkContext, SparkConf
from pyspark.streaming.kafka import KafkaUtils,TopicAndPartition
from pyspark.streaming import StreamingContext
from pyspark.storagelevel import StorageLevel
from pyspark.streaming import DStream
from pyspark.serializers import AutoBatchedSerializer, PickleSerializer, PairDeserializer,NoOpSerializer
import sys

# a,on local
conf =  SparkConf().setMaster("local[*]").setAppName("NetworkWordCount")
# b,standalone
# conf =  SparkConf().setMaster("spark://10.26.11.234:7077").setAppName("NetworkWordCount")
# c,yarn
# conf =  SparkConf().setMaster("yarn").setAppName("NetworkWordCount")
sc=SparkContext(conf=conf)
ssc = StreamingContext(sc,10)
# print(sys.argv)

# kvs = KafkaUtils.createStream(ssc,zkQuorum='192.168.1.100:9092',groupId="a",topics={b'loginhistory':2}).map(lambda  x:x)
#
# print(kvs.foreachRDD(lambda x:x.collect()))
# print(kvs)


# 使用socket接受消息
brokers='main:9092,suba:9092'
# lines=ssc.socketTextStream("192.168.1.100",9092)
# lines = KafkaUtils.createStream(ssc,zkQuorum='192.168.1.100:9092',groupId="a",topics={b'loginhistory':1},storageLevel=StorageLevel.MEMORY_AND_DISK_2)
lines = KafkaUtils.createDirectStream(ssc,['loginhistory'],kafkaParams={"metadata.broker.list":brokers})

counts=lines.map(lambda x:x[1]).flatMap(lambda x:x).map(lambda x:(x,1))
c2=counts.reduceByKey(lambda a,b:a+b)
print(type(c2))
# ssc.checkpoint("hdfs://main:9000/filetest/sparkkafkacheckpoint")
c2.pprint()
# #将结果保存到hdfs
# c2.saveAsTextFiles("hdfs://main:9000/filetest/sparkkafkaresultstore/")
# 将结果保存到kafka
c2.writetokafka
broker="main:9092"
k=KafkaClient(broker)
topic = k.topics[b'loginhistory_result']
produce = topic.get_sync_producer()
produce.produce(b'test')

ssc.start()

ssc.awaitTermination()