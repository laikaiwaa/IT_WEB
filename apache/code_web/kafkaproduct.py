from pykafka import KafkaClient,SimpleConsumer


# broker="192.168.159.132:9092"
broker="192.168.159.101:9092"
k=KafkaClient(broker)


#create_topic
topic = k.topics[b'loginhistory']
print(topic)

#produce
# produce=topic.get_producer()

for i in range(1):
    topic = k.topics[b'loginhistory']
    produce = topic.get_sync_producer()
    produce.produce(b'eeeedsddddddddddddddddddddddddddddddddddddd')
    produce.stop()
