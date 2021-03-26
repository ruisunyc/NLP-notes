import string
import random
import time

from kafka import KafkaProducer
if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    while 1:
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
        value = bytearray(word,'utf-8')        
        producer.send('wordcount-topic',value=value).get(timeout=10)
        #print(value)
        time.sleep(0.1)