#/root/tmp/sparkPython/reduceByKeyAndWindow.py
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
if __name__=='__main__':
    if len(sys.argv)!=3:
        print('<zk><topic>',file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName='reduceByKeyAndWindow')
    ssc = StreamingContext(sc,1)
    ssc.checkpoint('file:///root/tmp/sparkPython/checkpoint') #防止数据丢失
    lines = ssc.socketTextStream(sys.argv[1],int(sys.argv[2]))
    counts = lines.flatMap(lambda x:x.split(' ')).map(lambda x:(x,1)).reduceByKeyAndWindow(lambda a,b:a+b,lambda a,b:a-b,30,10) #func,inversefunc,滑动窗口大小30s，滑动窗口时间间隔10s
    counts.pprint()
    ssc.start()
    ssc.awaitTermination() 