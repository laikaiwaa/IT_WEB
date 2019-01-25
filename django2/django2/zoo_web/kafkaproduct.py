from pykafka import KafkaClient,SimpleConsumer

# broker="192.168.1.9:9092"
broker="localhost:9092"
k=KafkaClient(broker)


#create_topic
topic = k.topics[b'loginhistory']
print(topic)

#produce
produce=topic.get_sync_producer()
produce.produce(b'eeee')
produce.stop()