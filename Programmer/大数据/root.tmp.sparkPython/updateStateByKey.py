#/root/tmp/sparkPython/updateStateByKey.py
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
if __name__=='__main__':
    if len(sys.argv)!=3:
        print('<zk><topic>',file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName='StateWordCount')
    ssc = StreamingContext(sc,1)
    ssc.checkpoint('file:///root/tmp/sparkPython/stateful') #防止数据丢失
    initRDD = sc.parallelize([(u'hello',1),(u'world',1)])
    def updateFunc(new_values,last_sum):
        return sum(new_values)+(last_sum or 0)
    lines = ssc.socketTextStream(sys.argv[1],int(sys.argv[2]))
    counts = lines.flatMap(lambda x:x.split(' ')).map(lambda x:(x,1)).updateStateByKey(updateFunc,initialRDD=initRDD) 
    counts.pprint()
    ssc.start()
    ssc.awaitTermination() 