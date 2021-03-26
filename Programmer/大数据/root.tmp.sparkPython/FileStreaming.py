from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
conf = SparkConf()
conf.setAppName('TestDStream')
conf.setMaster('local[*]')
sc = SparkContext(conf = conf)
ssc = StreamingContext(sc,10) #每隔10s启动一次流计算
lines = ssc.textFileStream('file:///root/tmp/logfile')
words = lines.flatMap(lambda x:x.split(','))
wordsCounts = words.map(lambda x:(x,1)).reduceByKey(lambda a,b:a+b)
wordsCounts.pprint()
ssc.start()
ssc.awaitTermination()