#/root/tmp/sparkPython/spark__ss__filesource.py
#创建程序第数据进行统计

import os
import shutil
from pprint import pprint
from pyspark.sql import SparkSession
from pyspark.sql.functions import window,asc
from pyspark.sql.types import StructType,StructField
from pyspark.sql.types import TimestampType,StringType
#定义json文件的路径
TEST_DATA_DIR_SPARK='file:///root/tmp/file/testdata/'

if __name__ == '__main__':
    schema = StructType([StructField('eventTime',TimestampType(),True),
                         StructField('action',StringType(),True),
                         StructField('district',StringType(),True)])
    spark = SparkSession.builder.appName('structuredFileCount').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    lines = spark.readStream.format('json').schema(schema).option('maxFilesPerTrigger', 100).load(TEST_DATA_DIR_SPARK)  # 每读100个文件触发一次
    windowDuration = '1 minutes'

    windowedCounts = lines.filter("action='purchase'").groupBy('district',window('eventTime','1 minutes')).count().sort(asc('window'))
    query = windowedCounts.writeStream.outputMode('complete').format('console').option('truncate','false').trigger(
        processingTime='10 seconds').start()  # 执行流计算，显示到控制台，每隔10秒触发一次流计算

    query.awaitTermination()