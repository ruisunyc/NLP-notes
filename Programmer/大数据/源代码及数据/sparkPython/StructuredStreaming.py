# /root/tmp/sparkPython/StructuredStreaming.py 
from pyspark.sql import SparkSession
from pyspark.sql.functions import split,explode #拆分和展开数组


if __name__=='__main__':
    spark =SparkSession.builder.appName('StructuredStreaming').getOrCreate() #创建SparkSession对象
    spark.sparkContext.setLogLevel('WARN')
    lines = spark.readStream.format('socket').option('host','localhost').option('port',9999).load()#创建输入数据源
    words =lines.select(explode(split(lines.value,' ')).alias('word')) #dataframe列名为word
    wordCounts=words.groupBy('word').count() #按照列分组并计算词频
    query = wordCounts.writeStream.outputMode('complete').format('console').trigger(processingTime='8 seconds').start() #执行流计算，显示到控制台，每隔8秒触发一次流计算
    query.awaitTermination()
