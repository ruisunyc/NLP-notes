from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import time
if __name__=='__main__':  
    sc = SparkContext(appName = 'queneStream')
    ssc = StreamingContext(sc,10) #每隔10s不断计算
    rddQ = [] #创建队列
    for i in range(5):
        rddQ += [ssc.sparkContext.parallelize([j for j in range(1,100)],2)] #分2个区
        time.sleep(1)
	#创建RDD队列流
    inputStream = ssc.queueStream(rddQ)
    counts = inputStream.map(lambda x:(x%10,1)).reduceByKey(lambda a,b:a+b) #余数词频统计
    counts.pprint()
    ssc.start()
    ssc.stop(stopSparkContext=True,stopGraceFully=True)   