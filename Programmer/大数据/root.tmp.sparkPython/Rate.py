# 编写消费者程序
# /root/tmp/sparkPython/Rate.py
from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName('RateStream').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    lines = spark.readStream.format('rate').option('rowsPerSecond', 5).load() #每秒发送5行
    print(lines.schema)
    query=lines.writeStream.outputMode('update').format('console').option('truncate','false').start()
    query.awaitTermination()