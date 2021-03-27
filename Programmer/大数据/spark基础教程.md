## 大数据基础教程

[TOC]

## 一、[hdfs安装部署](https://www.cnblogs.com/youngchaolin/p/11992600.html )

- 心得

​		重点是免密登录从服务器节点，把主服务器密钥发给从服务器：在主服务器下运行 ssh-copy-id root@hadoop-slave1以及ssh-copy-id root@hadoop-slave2，在每个服务器都运行密钥发自己，自己也可以免密登录

- 防火墙配置

```shell
#安全模式

hadoop dfsadmin -safemode get #查看安全状态

hadoop dfsadmin -safemode leave #离开安全模式

#关闭防火墙（查看web 50070及8080失败，需要关闭）:

systemctl stop firewalld.service*#停止firewall* 

systemctl disable firewalld.service*#禁止firewall开机启动*
```

## 二、hadoop基础操作

```shell
ssh  hadoop-salve1 #登录到服务器hadoop-salve1

logout #退出服务器

hadoop fs -put tmp/a.txt / #把linux当前路径tmp文件夹下的文件放到 hadoop 的跟路径下

hadoop fs -ls / #查看根路径下的文件情况

hadoop fs -cat /a.txt #查看文件

hadoop fs -mkdir /test #创建文件夹

hadoop fs -mkdir -p /test/test1 #创建多级文件夹

hadoop fs -rm -r /test #删除文件夹

hdfs dfs -put /root/tmp/iris.csv / #上传文件到hdfs根目录下

jupyter notebook --ip 0.0.0.0 --allow-root #远程服务器打开jupyter

hive --service metastore & #运行hive之前执行
```

## 三、大数据时代

### 3.1 技术支撑

- 存储设备
- CPU计算能力（摩尔定律-》多核）
- 网络带宽

### 3.2 数据源生产方式

- 第一阶段 运营式系统阶段（eg.超市零售系统）
- 第二阶段 用户原创内容阶段（eg.知乎、豆瓣、微博）
- 第三阶段 感知式系统阶段（eg.传感器、摄像头、物联网采集）

###  3.3 大数据概念

特点：4V

- Volume 大量化（全球数据总量约 万亿GB=10亿TB=千万PB）

- Variety 多样化（10%结构化数据+90%非结构化数据）

- Velocity 快速化（推荐响应1秒内）

- Value 价值低（突发事件少，单点价值高）

###  3.4 大数据关键技术

- 分布式存储 HDFS/ HBASE/ Nosql /newSql
- 分布式计算 MapReduce/ Spark （微批处理秒级计算）/Flink（连续流毫秒级计算）

![image-20210314162102261](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314162102261.png)

![image-20210314172535717](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314172535717.png)

- Spark SQL：分析关系数据
- Spark/structured Streaming：流计算
- MLlib：机器学习算法库
- GraphX：编写图计算应用程序

MapReduce缺点：map/reduce模式表达有限、磁盘I/O（HDFS读取写入）开销大、反复迭代延迟高

Spark改进：

计算丰富、内存运行、DAG（有向无环图，为了容错，恢复数据，找父节点）任务调度执行机制

- 转换操作（不触发计算，只记录轨迹）：
	- Map
	- filter
	- groupBy
	- join
- 计算操作
	- reduce

思考：spark和Hadoop关系

spark可以替代Hadoop的mapReduce，与Hadoop中的hdfs配合使用

![image-20210314172731055](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314172731055.png)

## 四、Spark Core

![image-20210314173021016](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314173021016.png)

RDD（Resiliennt Distributed Datasets）

多台机器内存分区，弹性：计算过程中动态调整分区数量，数据少可分布在一台机器内存，数据多可分布在多台机器内存中

- 只读的分布式分区（对象）集合
- RDD依赖关系：
  - 窄依赖：出度1，入度多 【map,filter,union,join】，可进行流水线优化
  - 宽依赖：出度多（一个父亲多个儿子）【groupby,join】，发生了shuffle（洗牌）操作（会写磁盘），可划分成多个阶段，不能进行流水线优化

![image-20210314183544657](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314183544657.png)

DAG（有向无环图）:

![image-20210314173833456](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314173833456.png)

```python
from pyspark import SparkConf,SparkContext
conf = SparkConf().setMaster("local").setAppName('My APP')
sc.stop()
sc = SparkContext(conf=conf)
logData = sc.textFile( "file:///root/tmp/student.txt",2).cache() #file://表示本地路径，后面跟绝对路径位置，2表示分区数目，一般为CPU个数
numAs = logData.filter(lambda x:'1' in x).count()
numBs = logData.filter(lambda x:'C01' in x).count()
print(numAs,numBs)
```

### 4.1 spark集群安装

spark建立在hadoop基础上

Hadoop 主节点 namenode 对应 spark Driver节点 部署在同一台，方便管理

Hadoop 从节点 datanode 对应 spark Worker节点部署在同一台，方便本地化

先进入Hadoop目录下sbin目录，执行. start-all.sh脚本，启动Hadoop

再进入spark目录下sbin目录，执行. start-all.sh脚本，启动spark，

```shell
http://192.168.1.185:8080 # 打开spark网页
http://192.168.1.185:8088 # 打开Hadoop网页
```

![image-20210316163359652](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210316163359652.png)

- 在集群中运行pyspark

  ```shell
  ~/bigdata/spark/bin/pyspark --master spark://hadoop-master:7077 #进入pyspark交互环境
  ```
  

### 4.2 RDD创建

- sc.TextFile()方法

  ```python
  lines = sc.textFile( "file:///root/tmp/student.txt") #从本地master路径读取RDD,交互式环境默认sc创建好，sparkContext,spark的管理员
  lines = sc.textFile("hdfs://hadoop-master:9000/tmp/student.txt") #从hdfs加载数据
  lines = sc.textFile("/tmp/student.txt") #等价，从hdfs加载数据
  lines.take(5)#显示5条结果
  ```

- sc.parallelize()方法

  ```python
  array = [1,2,3] #python列表
  rdd = sc.parallelize(array,2) #并行集合,设置2个分区
  rdd.collect() #显示结果
  ```

### 4.3 RDD操作

#### Transformation(转换操作)

![image-20210316194154453](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210316194154453.png)

- filter(func)

  ```shell
  #student.txt
  C01,N0101,82
  C01,N0102,59
  C01,N0103,65
  C02,N0201,81
  C02,N0202,82
  C02,N0203,79
  C03,N0301,56
  C03,N0302,92
  ```

  ```python
  lines = sc.textFile("/tmp/student.txt") #生成RDD对象lines
  linesfilter = lines.filter(lambda line:'01' in line) #rdd.filter(func),跟Python filter类似
  linesfilter.collect() #显示结果
  ```

- map(func)

  ```python
  data = [1,2,3] #python列表
  rdd1 = sc.parallelize(data) # 转成RDD对象
  rdd1.map(lambda x:x+5).collect() #rdd.map(func)，跟Python map类似
  ```
  
- mapValues(func)

   ```python
   sc.parallelize([('a',1),('b',1),('c',1),('b',1),('b',1),('a',1)]).mapValues(lambda x:x+1).collect() #对value每个值进行map操作加1
   ```

- flatMap(func)

  ```python
  rdd = sc.textFile("/tmp/student.txt") #生成RDD对象lines
  rdd1= rdd.flatMap(lambda line:line.split(',')) #rdd.flatMap(func),先map再展平
  rdd2.collect() #显示结果
  ```
  
- groupByKey
  ```python
  sc.parallelize([('a',1),('b',1),('c',1),('b',1),('a',1)]).groupByKey().collect() #rdd.groupByKey(),返回(key，iterable(list))列表
 #返回(key，iterable),[('a', <pyspark.resultiterable.ResultIterable object at 0x7ffac2f987b8>), ('b', <pyspark.resultiterable.ResultIterable object at 0x7ffac2f987f0>), ('c', <pyspark.resultiterable.ResultIterable object at 0x7ffac2f98748>)] ,为RDD对象[('a',(1,1)),('b',(1,1)),('c',1)]
  ```
  
- reduceByKey(func)

  ```python
  sc.parallelize([('a',1),('b',1),('c',1),('b',1),('a',1)]).reduceByKey(lambda x,y:x+y).collect() #rdd.reduceByKey(func),统计分组后每个key对应values列表元素之和，[('a', 2), ('b', 2), ('c', 1)],先groupByKey再reduce
  #等价于
  sc.parallelize([('a',1),('b',1),('c',1),('b',1),('a',1)]).groupByKey().map(lambda t:(t[0],sum(t[1]))).collect() #[('a', (1, 1)), ('b', (1, 1)), ('c', 1)]
  sc.parallelize([('a',1),('b',1),('c',1),('b',1),('a',1)]).reduceByKey(lambda x,y:(x,)+(y,)).collect() #[('a', (1, 1)), ('b', (1, 1)), ('c', 1)]
  ```
  
 - sortByKey(func)

   ```python
   sc.parallelize([('a',1),('b',1),('c',1),('b',1),('a',1)]).sortByKey().collect() #按照key升序
   sc.parallelize([('a',1),('b',1),('c',1),('b',1),('a',1)]).reduceByKey(lambda a,b:a+b).sortByKey(False).collect() #统计词频按照key进行降序
   ```

- sortBy(func)

  ```python
  sc.parallelize([('a',1),('b',1),('c',1),('b',1),('b',1),('a',1)]).reduceByKey(lambda a,b:a+b).sortBy(lambda x:x[1],False).collect() #统计词频按照元素数量进行降序
  ```

- join

   ```python
   #   内连接（类似MySQL的inner join）
   rdd1 = sc.parallelize([('spark',1),('spark',2),('hadoop',3),('hadoop',5)])
   rdd2 = sc.parallelize([('spark','3')])
   rdd1.join(rdd2).collect() #[('spark', (1, '3')), ('spark', (2,'3'))]
   ```
   
 - keys()

   ```python
sc.parallelize([('a',1),('b',1),('c',1),('b',1),('a',1)]).keys().collect() #['a', 'b', 'c', 'b', 'a']
   ```

 - values

   ```python
sc.parallelize([('a',1),('b',1),('c',1),('b',1),('a',1)]).values().collect() #['a', 'b', 'c', 'b', 'a']
   ```

#### Action(行动操作)

  惰性机制(转换过程只记录转换的轨迹，行动操作才真正计算)

```python
count() #返回数据集中的元素个数
collect() #以数组形式返回数据集所有元素
first() #返回数据集第一个元素
take(n)#以数组形式返回数据集前n个元素
reduce(func)#通过函数func（输入两个参数返回一个值）聚合数据集中元素
forearch(func)#将数据集的每个元素传递到函数func中运行
```

```python
rdd = sc.parallelize([1,2,3,4,5])
rdd.count() #5
rdd.first() #1
rdd.take(3)#[1,2,3]
rdd.reduce(lambda x,y:x+y) #15
rdd.collect()#[1,2,3,4,5]
rdd.foreach(lambda x:print(x)) #并未显示？
lines = sc.textFile("/tmp/student.txt") #生成RDD对象lines,自动按换行符拆分成RDD列表对象
lines.collect() #['C01,N0101,82', 'C01,N0102,59', 'C01,N0103,65', 'C02,N0201,81', 'C02,N0202,82', 'C02,N0203,79', 'C03,N0301,56', 'C03,N0302,92', 'C03,N0306,72']
lineLeng = lines.map(lambda x:len(x))
lineLeng.collect()#[12, 12, 12, 12, 12, 12, 12, 12, 12]
totalLeng = lineLeng.reduce(lambda a,b:a+b)
totalLeng #108
```

### 4.4 RDD持久化

通过缓存机制避免重复计算（持久化后的RDD会保留在计算节点的内存中被后面的行动操作重复使用）

persist()

标记RDD为持久化，遇到第一个行动操作触发计算

```python
li = ['a','b','c']
rdd = sc.parallelize(li)
rdd.cache()#等价于rdd.persist(MEMORY_ONLY),只缓存在内存中，内存不足LRU替换，但并未真正缓存，要等到行动操作
rdd.count()#第一次行动，把rdd放到缓存中
'/'.join(rdd.collect()) #第二次行动，重复使用缓存的rdd
rdd.unpersist() #释放内存缓存的RDD
```

### 4.5 RDD分区

作用：

   -  并行计算
   -  减少通讯开销

原则：

   - 分区数量=集群中CPU核心数目

方法：

- 创建RDD时手动指定分区个数
- 通过转换操作得到新RDD时，直接调用repartition()方法
- 自定义分区(partitionBy(num,func)),num：分区个数，注意只接受(key,value)形式的RDD

```python
li = [1,2,3,4,5,6]
rdd = sc.parallelize(li,2) #设置2个分区
len(rdd.glom().collect()) #显示分区数量
rdd2=rdd.repartition(1) #重新分区为1
len(rdd2.glom().collect())#显示分区数量
```

需求1：根据key的最后一位数字，写到不同的文件

```python
func = lambda key:key%10 #最后一位数字即对key求模
data = sc.parallelize(range(100),2) #2个分区，[0,100)
data.map(lambda x:(x,1)) #先转化为键值对形式
.partitionBy(10,func) #重新对key进行求模，分成10个分区
.map(lambda x:x[0]) #再转化为键形式
.saveAsTextFile("file:///root/tmp/partitioner") #保存在本地/tmp/partitioner目录下，为10个文件part-00000，part-00001...
```

需求2：词频统计

```python
rdd = sc.textFile("/tmp/student.txt") #读取hdfs文件生成RDD对象rdd，也可以加载目录
rdd.flatMap(lambda x:x.split(',')).map(lambda x:(x,1)).reduceByKey(lambda a,b:a+b).collect()
```

需求3：统计每天平均销量

```python
rdd = sc.parallelize([('spark',2),('hadoop',6),('hadoop',4),('spark',6)])
rdd.groupByKey().map(lambda x:(x[0],sum(x[1])/len(x[1]))).collect()
# 等价于
rdd.mapValues(lambda x:(x,1)).reduceByKey(lambda a,b:(a[0]+b[0],a[1]+b[1])).mapValues(lambda x:x[0]/x[1]).collect()
```
需求4：文件排序

按文件数字排序，并增加递增索引列

```python
from pyspark import SparkConf,SparkContext
index = 0
def getindex():
    global index
    index+=1
    return index
def main():
    conf = SparkConf().setMaster('local').setAppName('FileSort')
    sc = SparkContext(conf=conf)
    lines = sc.textFile("file:///root/tmp/file/sort/file*.txt")
    lines.filter(lambda x:len(x.strip())>0).map(lambda x:(int(x.strip()),"")).repartition(1).sortByKey(True).map(lambda x:(getindex(),x[0])).saveAsTextFile("file:///root/tmp/file/filesort_res") #分成1个区全局有序
if __name__=='__main__':
    main()
```

需求5：多字段排序(待解决？)

对于给定的文件，按第一列降序，若相等按第二列降序

```shell
31 43
93 73
13 97
39 57
49 94
```

```python
from operator import gt
class SecondSortKey():
    def __init__(self,k):
        self.x = k[0]
        self.y = k[1]
    def __gt__(self,other):
        if self.x==other.x:
            return gt(self.y,other.y)
        return gt(self.x,other.x)   
rdd3 = sc.textFile("file:///root/tmp/file/sort/file3.txt").map(lambda x:((int(x.split()[0]),int(x.split()[1])),x))
rdd3.map(lambda x:(SecondSortKey(x[0]),x[1])).sortByKey(False).map(lambda x:x[1]).collect()
```

### 4.6 HBASE

hbase架构在hdfs上，是分布式数据库

- 启动：先启动hdfs，再启动hbase

```shell
cd ~/bigdata/hadoop
./sbin/start-all.sh #启动hdfs
cd ~/bigdata/hbase
./bin/start-hbase.sh
./bin/hbase shell #启动hbase
```

- 四维坐标定位：行键、列族、列限定符、版本时间戳

![image-20210319161502617](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210319161502617.png)

- hbase数据库添加数据

```python
name gender age
Xueqian F   23
Weiliang M   24
create 'student','info' #创建student表，列族info
put 'student','1','info:name','Xueqian' #插入单元格，student表，行键，列族：列限定符，单元格值
put 'student','1','info:gender','F' #插入单元格，student表，行键，列族：列限定符，单元格值
put 'student','1','info:age','23' #插入单元格，student表，行键，列族：列限定符，单元格值
put 'student','2','info:name','Weiliang' #插入单元格，student表，行键，列族：列限定符，单元格值
put 'student','2','info:gender','M' #插入单元格，student表，行键，列族：列限定符，单元格值
put 'student','2','info:age','24' #插入单元格，student表，行键，列族：列限定符，单元格值
```

## 五、Spark SQL

DataFrame

- 以RDD为基础的分布式数据集，可以处理大规模结构化数据

- SparkSession 指挥官 DataFrame

- SparkContext 指挥官 sparkCore

- 创建SparkSession 

  ```python
  from pyspark import SparkContext,SparkConf
  from pyspark.sql import SparkSession
  spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate() #指挥官，交互式环境自动创建sc和spark
  ```

### 5.1 创建DataFrame

  ```python
  spark.read.text('people.txt') #读取文本文件创建，本地file:///，hdfs://
  等价于spark.read.format('text').load('people.txt')
  spark.read.json('people.json')#读取json文件创建
  等价于spark.read.format('json').load('people.json')
  spark.read.parquet('people.parquet')#读取people.parquet文件创建
  等价于spark.read.format('parquet').load('people.parquet')
  ```

### 5.2 保存DataFrame

  ```python
  df.write.txt('people.txt') #保存为text目录
  等价于df.write.format('text').save('people.txt')
  df.write.json('people.json') #保存json目录
  等价于df.write.format('json').save('people.json')
  df.write.parquet('people.parquet')#保存parquet目录
  等价于df.write.format('parquet').save('people.parquet')
  ```

### 5.3 基本操作

  - show()

    ```python
    df = spark.read.json('file:///root/tmp/file/resources/people.json')
    df.show() #显示数据
    ```

  - printSchema()

    ```python
    df.printSchema() #打印表结构（模式）
    root
     |-- age: long (nullable = true)
     |-- name: string (nullable = true)
    ```

  - select()

    ```python
    df.select(df['name'],df['age']+1).show() #查询操作
    +----+---------+
    |name|(age + 1)|
    +----+---------+
    |   r|     null|
    |   s|       31|
    |   b|       26|
    +----+---------+
    ```

  - filter()

    ```python
    df.filter(df['age']<30).show() #过滤操作
    +---+----+
    |age|name|
    +---+----+
    | 25|   b|
    +---+----+
    ```

  - groupBy()

    ```python
    df.groupBy('age').count().show() #按年龄分组，并统计个数
    +----+-----+
    | age|count|
    +----+-----+
    |  25|    1|
    |null|    1|
    |  30|    1|
    +----+-----+
    ```

  - sort()

    ```python
    df.sort(df['age'].desc()).show() #按照年龄降序
    df.sort(df['age'].desc(),df['name'].asc()).show()#按照年龄降序，相同年龄按照姓名升序
    ```

- RDD转化DataFrame

  ```python
  from pyspark.sql import Row
  people = sc.textFile('file:///root/tmp/file/resources/people.txt').map(lambda x:x.split(',')).map(lambda x:Row(name=x[0],age=int(x[1])))
  people.collect()#[Row(age=29, name='s'), Row(age=30, name='a'), Row(age=19, name='b')]  
  schemaPeople = spark.createDataFrame(people) #RDD转为DataFrame
  schemaPeople.show()#已经成为dataFrame，可以显示数据表
  +---+----+
  |age|name|
  +---+----+
  | 29|   s|
  | 30|   a|
  | 19|   b|
  +---+----+
  schemaPeople.createOrReplaceTempView('people') #注册为临时表people
  personDF = spark.sql('select name,age from people where age>20') #people表执行sql查询
  personDF.show()
  personsRDD = personDF.rdd.map(lambda x:'Name:'+x.name+',Age:'+str(x.age)) #dataFrame每个元素为一行记录，包含name和age两个字段，分别用x.name和x.age获取
  personsRDD.collect()
  ```

- Spark SQL操作MySQL

  ```python
  jdbcDF = spark.read.format('jdbc').option('driver','com.mysql.jdbc.Driver').option('url','jdbc:mysql://192.168.1.192:3306/dataprocess').option('dbtable','bidtype1').option('user','root').option('password','Bibenet123456').load()  #读取MySQL数据表
  jdbcDF.show() #显示
  ######写入MySQL
  student = sc.parallelize(['11 100005 A 四川省巴中市南江县乐坝镇人民政府2016年乐坝镇棚户区改造政府购买服务项目公开招标采购公告','12 100005 A 四川省巴中市南江县乐坝镇人民政府2016年乐坝镇棚户区改造政府购买服务项目公开招标采购公告']).map(lambda x:x.split(' ')) #生成RDD
  rowRDD = student.map(lambda x:Row(id=int(x[0]),OBJECT_ID=int(x[1]),INDUSTRY_TYPE_FIRST=x[2],PROJECT_NAME=x[3])) #列表转成Row对象
  studentDF = spark.createDataFrame(rowRDD) #RDD转成DataFrame
  config = { 'user': 'root','password': 'Bibenet123456','driver':'com.mysql.jdbc.Driver'}
  studentDF.write.jdbc('jdbc:mysql://192.168.1.192:3306/dataprocess?useUnicode=true&characterEncoding=utf8','bidtype1','append',config)#写入MySQL
  ```


## 六、Spark 流计算

Spark Streaming

秒级微批处理

- Spark Core 数据抽象  RDD(管家：SparkContext)

- Spark SQL 数据抽象 DataFrame(管家：SparkSession)

- Streaming 数据抽象 DStream(管家：StreamingContext)（离散化discrete stream）
### 6.1 DStream创建
StreamingContext

  - pyspark环境

  ```python
  from pyspark.streaming import StreamingContext
  ssc = StreamingContext(sc,1) #每隔1s启动一次流计算
  ```

  - 独立streaming环境

  ```python
  from pyspark import SparkContext,SparkConf
  from pyspark.streaming import StreamingContext
  conf = SparkConf()
  conf.setAppName('TestDStream')
  conf.setMaster('local[*]')
  sc = SparkContext(conf = conf)
  ssc = StreamingContext(sc,1)
  ```

#### 文件流

/root/tmp/sparkPython/FileStreaming.py

```python
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
```

运行

```python
cd /root/bigdata/spark/bin
spark-submit /root/tmp/FileStreaming.py
```

#### 套接字流(Socket)

/root/tmp/sparkPython/socketCount.py

```python
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
```

  运行

  ```python
  /root/bigdata/spark/bin/spark-submit /root/tmp/sparkPython/socketCount.py localhost 9999
  ```

  服务端

  ```python
  # Linux netcat网络
  netstat -anp |grep 9999
  nc -lk 9999 #l:listen 监听 k：不断，服务端强制监听端口9999
  ```

  自定义服务端

  /root/tmp/sparkPython/SourceServer.py

  ```python
  import socket
  server = socket.socket() #创建socket对象
  server.bind(('localhost',9999)) #绑定ip和端口
  server.listen(1) #监听端口
  while 1:
      print('waiting conn...')
      conn,addr = server.accept()#阻塞等待客户端发送
      print('conn is success %s' % addr[0])
      print('send')
      conn.send('had,had,i,i,love'.encode())
      conn.close()
      print('conn is close')
  ```
#### RDD队列流

/root/tmp/sparkPython/queneCount.py

```python
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
```

#### Kafka数据源

- 高吞吐量的分布式发布订阅消息系统

- 同时满足在线实时处理和批量离线处理

- 数据交换枢纽

- 组件

  - Broker 多台服务器

  - Topic 按不同主题分开存储

  - Partition 每隔主题包含一个或多个Partition 

    ![image-20210322200351132](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210322200351132.png)

  - Producer 生产者 发布消息

  - Consumer 消费者 读取消息的客户端

    - Consumer Group 每个consumer 只属于某个Consumer Group

- 启动KafKa

  ```shell
  cd /root/bigdata/kafka
  ./bin/zookeeper-server-start.sh config/zookeeper.properties #启动zookeeper终端
  ```

  打开第二个终端

  ```shell
  cd /root/bigdata/kafka
  bin/kafka-server-start.sh config/server.properties#启动kafka终端
  ```

  测试

  ```python
  ./bin/kafka-topics.sh --zookeeper localhost:2181 --create --replication-factor 1 --partitions 1 --topic wordtest #1个副本1个分区
  ./bin/kafka-topics.sh --list --zookeeper localhost:2181 #展示
  ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic wordtest #用生产者Producer生产数据
  >hello hadoop
  >hello spark
  #打开新终端
  cd /root/bigdata/kafka
  ./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic wordtest --from-beginning #用Consumer查看
  ```

  编写kafka源流计算
  
  /root/tmp/sparkPython/kafkaCount.py
  
  ```python
  import sys
  from pyspark import SparkContext
  from pyspark.streaming import StreamingContext
  from pyspark.streaming.kafka import KafkaUtils
  if __name__=='__main__':
      if len(sys.argv)!=3:
          print('<zk><topic>',file=sys.stderr)
          exit(-1)
      sc = SparkContext(appName='KafkaWord')
      ssc = StreamingContext(sc,1)
      zkQuorum,topic = sys.argv[1:]
      kvs = KafkaUtils.createStream(ssc,zkQuorum,'spark-stream-consumer',{topic:1}) #构建输入源，spark-stream-consumer：spark-stream组,{topic:1}:主题:1个分区
      counts = kvs.map(lambda x:x[1]).flatMap(lambda x:x.split(' ')).map(lambda x:(word,1)).reduceByKey(lambda a,b:a+b)
      counts.pprint()
      ssc.start()
      ssc.awaitTermination()
  ```
  
  新建shell
  
  ```shell
   /root/bigdata/spark/bin/spark-submit /root/tmp/sparkPython/kafkaCount.py localhost:2181 WordCount
  ```
  
### 6.2 DStream转换操作

#### 无状态转换操作

只针对当前一个批次进行统计，历史数据不记录

如套接字流介绍的词频统计就采用的无状态转换，每次统计，都只统计当前批次到达的单词的词频，和之前批次无关，不会进行累计

```python
 - map(func)
 - flatMap(func)
 - filter(func)
 - repartition(numPartitions)   #分区改变并行程度
 - reduce(func)   #聚合
 - count()  # 统计源DStream中RDD元素数量
- union(otherStream) #合并DStream
  - reduceByKey(func,[numTasks]) #key相同，进行聚合运算，返回新(K,V)组成的DStream
- join(otherStream,[numTasks]) # 拼接相同key的v,返回(k,(V,W))键值对
```

#### 有状态转换操作

- 滑动窗口转换操作(reduceByKeyAndWindow())

  ```python
  reduceByKeyAndWindow(func,windowLength,slideInterval,[numTasks]) #应用到(k,v)键值对组成的DStream上，通过numTasks参数的设置来指定不同的任务数
  reduceByKeyAndWindow(func,invFunc,windowLength,slideInterval,[numTasks]) #更加高效，增量计算，优化的是窗口内的计算量，减少计算量，对进入窗口内的新数据进行reduce操作，并对离开窗口的老数据进行“逆向reduce”操作。
  ```

  ```python
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
  ```

  测试

  ```shell
  nc -lk 9999 #启动服务端socket,数据源终端
  #再启动shell，流计算终端
  /root/bigdata/spark/bin/spark-submit /root/tmp/sparkPython/reduceByKeyAndWindow.py localhost 9999
  ```

- updateStateByKey操作

  跨批次之间维护状态

  ```python
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
  ```

  测试

  ```python
  nc -lk 9999 #启动服务端socket,数据源终端
  #再启动shell，流计算终端
  /root/bigdata/spark/bin/spark-submit /root/tmp/sparkPython/updateStateByKey.py localhost 9999
  ```

  - DStream输出转化
  
    - saveAsTextFiles（DStream输出到文本文件）
    
      ```python
      #/root/tmp/sparkPython/fileOut.py
      import sys
      from pyspark import SparkContext
      from pyspark.streaming import StreamingContext
      if __name__=='__main__':
          if len(sys.argv)!=3:
              print('<zk><topic>',file=sys.stderr)
              exit(-1)
          sc = SparkContext(appName='StateWordCountFile')
          ssc = StreamingContext(sc,1)
          ssc.checkpoint('file:///root/tmp/sparkPython/statefulFile/') #防止数据丢失
          initRDD = sc.parallelize([(u'hello',1),(u'world',1)])
          def updateFunc(new_values,last_sum):
              return sum(new_values)+(last_sum or 0)
          lines = ssc.socketTextStream(sys.argv[1],int(sys.argv[2]))
          counts = lines.flatMap(lambda x:x.split(' ')).map(lambda x:(x,1)).updateStateByKey(updateFunc,initialRDD=initRDD) 
          counts.saveAsTextFiles('file:///root/tmp/sparkPython/statefulFile/output') #保存到文件
          counts.pprint()
          ssc.start()
          ssc.awaitTermination() 
      ```
    
    - DStream写入到MySQL
    
      ```python
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
      ```
    
      测试
    
      ```python
      netstat -anp |grep 9999
      nc -lk 9999 #启动服务端socket,数据源终端
      #再启动shell，流计算终端
      /root/bigdata/spark/bin/spark-submit /root/tmp/sparkPython/networkWordStatulDB.py localhost 9999
      ```


## 七、结构化数据流 

### 7.1 Structured Streaming

思想：将实时数据流视为一张正在不断添加数据的表

- 微批处理模式

  默认使用微批处理执行模型（延迟100ms+），spark流计算引擎会周期检查流数据源，对上一批次结束后到达的新数据执行批量查询

- 持续处理模式（spark 2.3.0+，毫秒级延迟），已处理数据的偏移量异步写入预写日志，启动一系列连续读取、处理和写入结果的长时间运行任务

和Spark Streaming区别

- Structured Streaming 采用的数据抽象是DataFrame

  Spark Streaming采用的数据抽象是DStream(本质还是RDD)

- Structured Streaming处理结构化的数据流

  Spark SQL处理静态的数据

- Structured Streaming可以实现毫秒级响应，可以对DataFrame/Dataset应用操作select/where/groupBy/map/filter/flatMap

  Spark Streaming 实现的是秒级响应

编程案例

包含很多行英文语句的数据流源源不断到达，Structured Streaming程序对每行进行拆分统计词频

```python 
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
```

```shell
#测试
netstat -anp |grep 9999
nc -lk 9999 #启动服务端socket,数据源终端
#再启动shell，流计算终端
/root/bigdata/spark/bin/spark-submit /root/tmp/sparkPython/StructuredStreaming.py
```

### 7.2 输入源

#### File源

支持csv/json/orc/parquet/text

```python
#/root/tmp/sparkPython/StructuredStreamingJSON.py
#生成测试文件
import os
import shutil
import random
import time

TEST_DATA_TEMP_DIR = '/root/tmp/file/'
TEST_DATA_DIR = '/root/tmp/file/testdata/'
ACTION_DEF = ['login', 'logout', 'purchase']
DISTRICT_DEF = ['fujian', 'beijing', 'shanghai', 'guangzhou']
JSON_LINE_PATTERN = '{{"eventTime":{},"action":"{}","district":"{}"}}\n'


# 测试环境搭建，创建文件夹
def test_setUp():
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR, ignore_errors=True)
    os.mkdir(TEST_DATA_DIR)


# 测试环境清空
def test_tearDown():
    if os.path.exists(TEST_DATA_DIR):
        shutil.rmtree(TEST_DATA_DIR, ignore_errors=True)


# 生成测试文件
def write_and_move(filename, data):
    with open(TEST_DATA_TEMP_DIR + filename, 'wt', encoding='utf-8') as f:
        f.write(data)
    shutil.move(TEST_DATA_TEMP_DIR + filename, TEST_DATA_DIR + filename)


if __name__ == '__main__':
    test_setUp()
    for i in range(1000):
        filename = 'e_mall_{}.json'.format(i)
        content = ''
        rndcount = list(range(100))
        random.shuffle(rndcount)
        for _ in rndcount:
            content += JSON_LINE_PATTERN.format(str(int(time.time())), random.choice(ACTION_DEF),
                                                random.choice(DISTRICT_DEF))
        write_and_move(filename,content)
        time.sleep(1)
    test_tearDown()

```

```python
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
```

测试

```shell
#新建终端
source activate py365
python /root/tmp/sparkPython/StructuredStreamingJSON.py
#再新建终端
/root/bigdata/spark/bin/spark-submit /root/tmp/sparkPython/spark__ss__filesource.py
```

#### Kafka源

  生产者每0.1秒生成包含2个字母的单词，并写入'wordcount-topic'的主题内，

  消费者订阅wordcount-topic，会源源不断收到单词，每隔8秒进行一次词频统计，把统计结果输出到主题wordcount-result-topic内，并通过2个监控程序检查

  ```shell
  #step1:新建终端,启动zookeeper终端
  cd /root/bigdata/kafka
  ./bin/zookeeper-server-start.sh config/zookeeper.properties
  #step2:再新建终端,启动kafka终端
  cd /root/bigdata/kafka
  bin/kafka-server-start.sh config/server.properties
  #step3:再新开终端，监控kafka收到的文本,监控输入终端
  cd /root/bigdata/kafka
  bin/kafka-console-consumer.sh --bootstrap-server  localhost:9092 --topic wordcount-topickafka
  #step4:再新开终端，监控输出的结果文本,#启动kafka监控输入终端
  cd /root/bigdata/kafka
  bin/kafka-console-consumer.sh --bootstrap-server  localhost:9092 --topic wordcount-result-topic
  ```

  ```python
  #编写生产者程序
  #/root/tmp/sparkPython/kafka_structed_producer.py
  import string
  import random
  import time
  
  from kafka import KafkaProducer
  if __name__ == '__main__':
      producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
      while 1:
          word = ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
          value = bytearray(word,'utf-8')
          producer.send('wordcount-topic',value=value).get(timeout=10)
          time.sleep(0.1)
  ```

  ```shell
  #启动执行
  source activate py365
  pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -U kafka-python #安装包
  python /root/tmp/sparkPython/kafka_structed_producer.py #运行生产者程序
  ```

  ```python
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
  
  ```

  ```shell
  #启动消费者
  /root/bigdata/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 /root/tmp/sparkPython/kafka_structed_consumer.py
  ```

#### Socket源

  从一个本地或远程主机的某个端口服务上读取数据，编码为utf-8，使用内存保存，不能提供端到端的容错保障。一般用于测试或学习。

#### Rate源

  每秒生成特定个数的数据行，数据格式为时间戳和开始到当前发送消息的总个数，一般用于调试和性能基准测试。

  ```python
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
  ```

### 7.3 输出操作

writeSteam()

将会返回DataStreamWriter接口，接口通过.start()启动流计算

  ```python 
  format:#接收器类型
  outputMode:#输出模式，可以是Append模式、Complete模式或Update模式
  #Append模式
  #追加模式，不更改结果表中现有行的内容
  #Complete模式
  #完全写入模式
  #Update模式
  #更新的行存储
  queryName:#查询的名称
  trigger:#触发间隔，处理超时超过触发间隔，则处理完成后立即触发新查询
  ```
## 八、Spark  MLlib

基于大数据的机器学习

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210327093058868.png)

spark.mllib 基于RDD

saprk.ml 基于DataFrame

### 8.1 流水线

```python
#判断文本是否包含spark单词
# /root/tmp/sparkPython/sparkLR.py
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF,Tokenizer
if __name__ == '__main__':    
    spark=SparkSession.builder.master('local').appName('WordCountML').getOrCreate()
    training = spark.createDataFrame([(0,'a b c d spark',1.0),(1,'b d',0.0),(2,'spark f',1.0),(3,'hadd map',0.0)],['id','text','label'])
    tokenizer = Tokenizer(inputCol='text',outputCol='words')
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(),outputCol='features')
    lr = LogisticRegression(maxIter=10,regParam=0.001)
    pipeline = Pipeline(stages=[tokenizer,hashingTF,lr]) #构建流水线
    model = pipeline.fit(training) #训练
    test = spark.createDataFrame([(4,'spark'),(5,'b'),(6,'f spark '),(7,'apache hadoop')],['id','text'])
    prediction = model.transform(test) #预测
    select = prediction.select('id','text','probability','prediction')
    for row in select.collect():
        rid,text,probablity,predic =row
        print(rid,text,probablity,predic)
```

```shell
  #测试运行
  /root/bigdata/spark/bin/spark-submit /root/tmp/sparkPython/sparkLR.py
  #结果
  4 spark [0.037824300992817445,0.9621756990071826] 1.0
  5 b [0.9644660707560256,0.03553392924397423] 0.0
  6 f spark  [0.00262976838891869,0.9973702316110812] 1.0
  7 apache hadoop [0.7847258548694875,0.21527414513051252] 0.0
```

### 8.2 特征提取和转换

```python
StringIndexer #字符串转整数索引，索引按照标签频率降序从0开始编码
IndexToString #整数索引转字符串
OneHotEncoder #独热编码
VectorIndexer #向量转类别编码
```

```python
#StringIndexer 实例
from pyspark.ml.feature import StringIndexer 
from pyspark.sql import SparkSession
spark=SparkSession.builder.master('local').appName('WordCountIndex').getOrCreate()
df = spark.createDataFrame([(0,'a'),(1,'b'),(2,'c'),(3,'a'),(4,'a'),(5,'c')],['id','category'])
indexer = StringIndexer(inputCol='category',outputCol='cateIndex') #新增一列cateIndex
model = indexer.fit(df)
indexed = model.transform(df)
indexed.show()
#IndexToString实例
from pyspark.ml.feature import IndexToString
toString = IndexToString(inputCol='cateIndex',outputCol='originCate') #新增一列originCate
indexString = toString.transform(indexed)
indexString.select('id','originCate').show()
#VectorIndexer实例
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.linalg import Vector,Vectors
df = spark.createDataFrame([(Vectors.dense(-1.0,1.0,1.0),),(Vectors.dense(-1.0,3.0,1.0),),(Vectors.dense(0.0,5.0,1.0),)],['features'])
indexer = VectorIndexer(inputCol='features',outputCol='indexed',maxCategories=2)#单列不同值的个数<=2的进行转化
indexerModel = indexer.fit(df)
indexVectored = indexerModel.transform(df)
indexVectored.show()
```

```shell
#indexed.show()
+---+--------+---------+
| id|category|cateIndex|
+---+--------+---------+
|  0|       a|      0.0|
|  1|       b|      2.0|
|  2|       c|      1.0|
|  3|       a|      0.0|
|  4|       a|      0.0|
|  5|       c|      1.0|
+---+--------+---------+
#indexString.select('id','originCate').show()
+---+----------+
| id|originCate|
+---+----------+
|  0|         a|
|  1|         b|
|  2|         c|
|  3|         a|
|  4|         a|
|  5|         c|
+---+----------+
#indexVectored.show()
+--------------+-------------+
|      features|      indexed|
+--------------+-------------+
|[-1.0,1.0,1.0]|[1.0,1.0,0.0]|
|[-1.0,3.0,1.0]|[1.0,3.0,0.0]|
| [0.0,5.0,1.0]|[0.0,5.0,0.0]|
+--------------+-------------+
```

### 8.3 TF-IDF

  ```python
  from pyspark.ml.feature import HashingTF,IDF,Tokenizer
  from pyspark.sql import SparkSession
  #创建DataFrame,每个句子代表一个文档
  if __name__ == '__main__':    
      spark=SparkSession.builder.master('local').appName('WordCountTFIDF').getOrCreate()
      sentenceData = spark.createDataFrame([(0,'I love you'),(0,'I love beijing'),(1,'logistic regression models')]).toDF('label','sentence')
      tokenizer = Tokenizer(inputCol='sentence',outputCol='words')
      wordsData = tokenizer.transform(sentenceData)
      wordsData.show()
      hashingTF = HashingTF(inputCol='words',outputCol='rawFeatures',numFeatures=2000) #哈希表桶数为2000
      featurizedData = hashingTF.transform(wordsData)
      featurizedData.select('words','rawFeatures').show(truncate=False)
      idf=IDF(inputCol='rawFeatures',outputCol='features')
      model = idf.fit(featurizedData) #训练
      rescaledData = model.transform(featurizedData) #转化
      rescaledData.select('label','features').show(truncate=False)
  ```

  ```python
  #wordsData.show()
  +-----+--------------------+--------------------+
  |label|            sentence|               words|
  +-----+--------------------+--------------------+
  |    0|          I love you|      [i, love, you]|
  |    0|      I love beijing|  [i, love, beijing]|
  |    1|logistic regressi...|[logistic, regres...|
  +-----+--------------------+--------------------+
  #featurizedData.select('words','rawFeatures').show(truncate=False)
  +------------------------------+------------------------------------+
  |words                         |rawFeatures                         |
  +------------------------------+------------------------------------+
  |[i, love, you]                |(2000,[240,1329,1425],[1.0,1.0,1.0])|
  |[i, love, beijing]            |(2000,[240,862,1329],[1.0,1.0,1.0]) |
  |[logistic, regression, models]|(2000,[695,1193,1604],[1.0,1.0,1.0])|
  +------------------------------+------------------------------------+
  #rescaledData.select('label','features').show(truncate=False)
  +-----+-----------------------------------------------------------------------------------+
  |label|features                                                                           |
  +-----+-----------------------------------------------------------------------------------+
  |0    |(2000,[240,1329,1425],[0.28768207245178085,0.28768207245178085,0.6931471805599453])|
  |0    |(2000,[240,862,1329],[0.28768207245178085,0.6931471805599453,0.28768207245178085]) |
  |1    |(2000,[695,1193,1604],[0.6931471805599453,0.6931471805599453,0.6931471805599453])  |
  +-----+-----------------------------------------------------------------------------------+
  ```

### 8.4 逻辑斯谛回归

  ```python
from pyspark.ml.linalg import Vector, Vectors
from pyspark.sql import Row, functions
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.classification import LogisticRegression


def f(x):
    # x列表
    rel = {}
    rel['features'] = Vectors.dense(float(x[0]), float(x[1]), float(x[2]), float(x[3]))
    rel['label'] = str(x[4])
    return rel


if __name__ == '__main__':

    spark = SparkSession.builder.master('local').appName('LogisticRegression').getOrCreate()
    data = spark.sparkContext.textFile('file:///root/tmp/sparkPython/data/iris.txt').map(lambda x: x.split('\t')).map(
        lambda p: Row(**f(p))).toDF()
    # data.show()
    # 标签列和特征列，进行索引并重命名
    labelIndexer = StringIndexer().setInputCol('label').setOutputCol('indexedLabel').fit(data)
    featureIndexer = VectorIndexer().setInputCol('features').setOutputCol('indexedFeatures').fit(data)
    # 构建LogisticRegression参数
    lr = LogisticRegression().setLabelCol('indexedLabel').setFeaturesCol('indexedFeatures').setMaxIter(100).setRegParam(
        0.3).setElasticNetParam(0.8)  # 迭代次数100次，规划化项0.3
    # print(lr.explainParams())
    # 结果数字转字符串
    labelConverter = IndexToString().setInputCol('prediction').setOutputCol('predicredLabel').setLabels(
        labelIndexer.labels)
    # 构建流水线
    lrPipeline = Pipeline().setStages([labelIndexer, featureIndexer, lr, labelConverter])
    trainingData, testData = data.randomSplit([0.7, 0.3])
    lrModel = lrPipeline.fit(trainingData)  # 训练得到model，为转化器
    lrPred = lrModel.transform(testData)  # 预测，生成新DataFrame
    # 打印结果
    preRel = lrPred.select('predicredLabel', 'label', 'features', 'probability').collect()
    for item in preRel:
        print(str(item['label']), str(item['features']), str(item['probability']), str(item['predicredLabel']))
        # 评估
        evaluator = MulticlassClassificationEvaluator().setLabelCol("indexedLabel").setPredictionCol('prediction')
        lrAcc = evaluator.evaluate(lrPred)
  ```

  ```shell
    #data.show()
    +-----------------+-----------+
  |         features|      label|
    +-----------------+-----------+
    |[5.1,3.5,1.4,0.2]|Iris-setosa|
    |[4.9,3.0,1.4,0.2]|Iris-setosa|
    |[4.7,3.2,1.3,0.2]|Iris-setosa|
    |[4.6,3.1,1.5,0.2]|Iris-setosa|
    |[5.0,3.6,1.4,0.2]|Iris-setosa|
    |[5.4,3.9,1.7,0.4]|Iris-setosa|
    |[4.6,3.4,1.4,0.3]|Iris-setosa|
  ```

### 8.5 决策树分类器

  ```python
  #/root/tmp/sparkPython/DecisionTreeClassifier.py
  from pyspark.sql import SparkSession
  from pyspark.ml.classification import DecisionTreeClassifier
  from pyspark.ml import Pipeline, PipelineModel
  from pyspark.ml.evaluation import MulticlassClassificationEvaluator
  from pyspark.ml.linalg import Vector, Vectors
  from pyspark.sql import Row
  from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer, HashingTF, Tokenizer
  
  
  def f(x):
      # x列表
      rel = {}
      rel['features'] = Vectors.dense(float(x[0]), float(x[1]), float(x[2]), float(x[3]))
      rel['label'] = str(x[4])
      return rel
  
  
  if __name__ == '__main__':
      spark = SparkSession.builder.master('local').appName('LogisticRegression').getOrCreate()
  
      data = spark.sparkContext.textFile('file:///root/tmp/sparkPython/data/iris.txt').map(lambda x: x.split('\t')).map(
          lambda p: Row(**f(p))).toDF()
      labelIndexer = StringIndexer().setInputCol('label').setOutputCol('indexedLabel').fit(data)
      featureIndexer = VectorIndexer().setInputCol('features').setOutputCol('indexedFeatures').setMaxCategories(4).fit(
          data)
      # 标签列和特征列，进行索引并重命名
      labelConverter = IndexToString().setInputCol('prediction').setOutputCol('predicredLabel').setLabels(
          labelIndexer.labels)
      trainingData, testData = data.randomSplit([0.7, 0.3])
      dtClassifier = DecisionTreeClassifier().setLabelCol('indexedLabel').setFeaturesCol('indexedFeatures')
      dtPipeline = Pipeline().setStages([labelIndexer, featureIndexer, dtClassifier, labelConverter])
      dtModel = dtPipeline.fit(trainingData)
      dtPredictions = dtModel.transform(testData)
      dtPredictions.select('predicredLabel', 'label', 'features').show(10)
      evaluator = MulticlassClassificationEvaluator().setLabelCol('indexedLabel').setPredictionCol('prediction') #原始数字标签和预测标签比较
      dtAccuracy = evaluator.evaluate(dtPredictions)
      print(dtAccuracy)
      treeModelClassifier = dtModel.stages[2] #第3个索引
      print(str(treeModelClassifier.toDebugString))
  
  ```

  ```shell
  #测试运行
  source activate py365
  python /root/tmp/sparkPython/DecisionTreeClassifier.py
  #spark-submit方式
  /root/bigdata/spark/bin/spark-submit /root/tmp/sparkPython/DecisionTreeClassifier.py
  ```

  ```shell
  +---------------+---------------+-----------------+
    | predicredLabel|          label|         features|
  +---------------+---------------+-----------------+
    |    Iris-setosa|    Iris-setosa|[4.6,3.4,1.4,0.3]|
    |    Iris-setosa|    Iris-setosa|[4.7,3.2,1.3,0.2]|
    |    Iris-setosa|    Iris-setosa|[4.7,3.2,1.6,0.2]|
    |    Iris-setosa|    Iris-setosa|[4.8,3.0,1.4,0.1]|
    |    Iris-setosa|    Iris-setosa|[4.8,3.4,1.6,0.2]|
    |Iris-versicolor|Iris-versicolor|[4.9,2.4,3.3,1.0]|
    |    Iris-setosa|    Iris-setosa|[4.9,3.1,1.5,0.1]|
    |Iris-versicolor|Iris-versicolor|[5.0,2.3,3.3,1.0]|
    |    Iris-setosa|    Iris-setosa|[5.0,3.3,1.4,0.2]|
    |    Iris-setosa|    Iris-setosa|[5.0,3.5,1.3,0.3]|
    +---------------+---------------+-----------------+
    only showing top 10 rows
    
    0.9454886576837795
    DecisionTreeClassificationModel (uid=DecisionTreeClassifier_473c804cbf7e9a80ef90) of depth 4 with 9 nodes
      If (feature 2 <= 1.9)
       Predict: 0.0
      Else (feature 2 > 1.9)
       If (feature 3 <= 1.6)
        If (feature 2 <= 4.9)
         Predict: 1.0
        Else (feature 2 > 4.9)
         If (feature 0 <= 6.0)
          Predict: 1.0
         Else (feature 0 > 6.0)
          Predict: 2.0
       Else (feature 3 > 1.6)
        Predict: 2.0
  ```
## 九、参考资料

本教程主要参考厦门大学林教授的[视频](!https://www.bilibili.com/video/BV1oE411s7h7)亲自编写制作而成，大数据环境配置主要参考[黑马人工智能](!https://www.bilibili.com/video/BV1Yf4y117iC?from=search&seid=3459936430251610080)部分课程

这些视频质量相对较高，但内容也比较多，大家可以根据自己掌握的情况适当补充学习