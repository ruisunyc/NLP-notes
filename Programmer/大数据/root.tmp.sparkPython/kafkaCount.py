import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
if __name__=='__main__':
    if len(sys.argv)!=3:
        print('<zk><topic>',file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName='KafkaWord')
    ssc = StreamingContext(sc,1)
    zkQuorum,topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc,zkQuorum,'spark-stream-consumer',{topic:1}) #构建输入源，spark-stream-consumer：spark-stream组,{topic:1}:主题:1个分区
    counts = kvs.map(lambda x:x[1]).flatMap(lambda x:x.split(' ')).map(lambda x:(word,1)).reduceByKey(lambda a,b:a+b)
    counts.pprint()
    ssc.start()
    ssc.awaitTermination()   