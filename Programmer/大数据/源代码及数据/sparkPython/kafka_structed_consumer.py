# 编写消费者程序
# /root/tmp/sparkPython/kafka_structed_consumer.py
from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName('strucedKafkaWordCount').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    lines = spark.readStream.format('kafka').option('kafka.bootstrap.servers', 'localhost:9092').option('subscribe',
                                                                                                        'wordcount-topic').load().selectExpr(
        'CAST(value AS STRING)')
    wordCounts = lines.groupBy('value').count()
    query = wordCounts.selectExpr("CAST(value AS STRING) as key",
                                  "CONCAT(CAST(value AS STRING)),':',CAST(count AS STRING) as value").writeStream.outputMode(
        'complete').format('kafka').option('kafka.bootstrap.servers', 'localhost:9092').option('topic',
                                                                                               'wordcount-result-topic').option(
        "checkpointLocation", "file:///root/tmp/kafka-sink-cp").trigger(
        processingTime='8 seconds').start()  # 执行流计算，显示到控制台，每隔10秒触发一次流计算

    query.awaitTermination()
