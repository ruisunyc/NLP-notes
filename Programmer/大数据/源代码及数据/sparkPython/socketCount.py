from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
import sys
if __name__=='__main__':
    if len(sys.argv)!=3:
        exit(-1)
    sc = SparkContext(appName = 'WordCount')
    ssc = StreamingContext(sc,1)
    lines = ssc.socketTextStream(sys.argv[1],int(sys.argv[2]))
    counts = lines.flatMap(lambda x:x.split(',')).map(lambda x:(x,1)).reduceByKey(lambda a,b:a+b)
    counts.pprint()
    ssc.start()
    ssc.awaitTermination()