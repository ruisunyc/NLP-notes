# /root/tmp/sparkPython/networkWordStatulDB.py
#source activate py365
import sys
import pymysql
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


def dbfunc(records):
    db = pymysql.connect('192.168.1.192', 'root', 'Bibenet123456', 'dataprocess')
    cursor = db.cursor()

    def doinsert(p):
        sql = '''insert into wordcount(word,count) values ('%s','%s')''' % (str(p[0]), str(p[1]))
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    for item in records:
        doinsert(item)


def func(rdd):
    repartitionedRDD = rdd.repartition(3)  # 减少分区，减少并发连接数据库
    repartitionedRDD.foreachPartition(dbfunc)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('<zk><topic>', file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName='StateWordCountDB')
    ssc = StreamingContext(sc, 1)
    ssc.checkpoint('file:///root/tmp/sparkPython/statefulDB/')  # 防止数据丢失
    initRDD = sc.parallelize([(u'hello', 1), (u'world', 1)])


    def updateFunc(new_values, last_sum):
        return sum(new_values) + (last_sum or 0)


    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    counts = lines.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).updateStateByKey(updateFunc,
                                                                                          initialRDD=initRDD)
    counts.foreachRDD(func)  # 保存到数据库
    counts.pprint()
    ssc.start()
    ssc.awaitTermination()