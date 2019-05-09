from pykafka import KafkaClient,SimpleConsumer

broker="192.168.159.100:9092"
# broker="192.168.159.134:9092"
# broker="localhost:9092"
k=KafkaClient(broker)
print(k.brokers)

#create_topic
# topic = k.topics[b'loginhistory']
topic = k.topics[b'loginhistory_result']
print(topic)


#comsumer
consumer=topic.get_simple_consumer(consumer_group=b'loginhistory', auto_commit_enable=True, auto_commit_interval_ms=1,consumer_id=b'test1')
for each in consumer:
    print(each)
    print(each.offset)
    print(each.value)
consumer.stop()