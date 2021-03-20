### 一、[hdfs安装部署](https://www.cnblogs.com/youngchaolin/p/11992600.html )

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

### 二、hadoop基础操作

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

### 三、大数据时代

### 技术支撑

- 存储设备
- CPU计算能力（摩尔定律-》多核）
- 网络带宽

### 数据源生产方式

- 第一阶段 运营式系统阶段（eg.超市零售系统）
- 第二阶段 用户原创内容阶段（eg.知乎、豆瓣、微博）
- 第三阶段 感知式系统阶段（eg.传感器、摄像头、物联网采集）

## 大数据概念

特点：4V

- Volume 大量化（全球数据总量约 万亿GB=10亿TB=千万PB）

- Variety 多样化（10%结构化数据+90%非结构化数据）

- Velocity 快速化（推荐响应1秒内）

- Value 价值低（突发事件少，单点价值高）

## 大数据关键技术

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
## spark应用

![image-20210314172731055](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314172731055.png)



## spark基本概念

![image-20210314173021016](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314173021016.png)

RDD（Resiliennt Distributed Datasets）：（多台机器内存分区，弹性：计算过程中动态调整分区数量），数据少可分布在一台机器内存，数据多可分布在多台机器内存中

- 只读的分布式分区（对象）集合
- RDD依赖关系：
  - 窄依赖：出度1，入度多 【map,filter,union,join】，可进行流水线优化
  - 宽依赖：出度多（一个父亲多个儿子）【groupby,join】，发生了shuffle（洗牌）操作（会写磁盘），可划分成多个阶段，不能进行流水线优化

![image-20210314183544657](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314183544657.png)

DAG（有向无环图）:

![image-20210314173833456](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314173833456.png)

### Demo

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

### spark集群安装

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
  

### RDD创建

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

### RDD操作

 - Transformation(转换操作)

   ![image-20210316194154453](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210316194154453.png)

   

   

   ```python
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

   - filter(func)

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
    ```
    - join
      内连接（类似MySQL的inner join）
      ```python
      rdd1 = sc.parallelize([('spark',1),('spark',2),('hadoop',3),('hadoop',5)])
      rdd2 = sc.parallelize([('spark','3')])
      rdd1.join(rdd2).collect() #[('spark', (1, '3')), ('spark', (2, '3'))]
    ```
   
    - keys()
   
      ```python
      sc.parallelize([('a',1),('b',1),('c',1),('b',1),('a',1)]).keys().collect() #['a', 'b', 'c', 'b', 'a']
      ```
   
    - values
   
      ```python
      sc.parallelize([('a',1),('b',1),('c',1),('b',1),('a',1)]).values().collect() #['a', 'b', 'c', 'b', 'a']
      ```
   
      


 - Action(行动操作)

  惰性机制(转换过程只记录转换的轨迹，行动操作才真正计算)

  - count() #返回数据集中的元素个数

  - collect() #以数组形式返回数据集所有元素

  - first() #返回数据集第一个元素

  - take(n)#以数组形式返回数据集前n个元素

  - reduce(func)#通过函数func（输入两个参数返回一个值）聚合数据集中元素

  - forearch(func)#将数据集的每个元素传递到函数func中运行

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

### RDD持久化

通过缓存机制避免重复计算（持久化后的RDD会保留在计算节点的内存中被后面的行动操作重复使用）

- persist()

  标记RDD为持久化，遇到第一个行动操作触发计算

  ```python
  li = ['a','b','c']
  rdd = sc.parallelize(li)
  rdd.cache()#等价于rdd.persist(MEMORY_ONLY),只缓存在内存中，内存不足LRU替换，但并未真正缓存，要等到行动操作
  rdd.count()#第一次行动，把rdd放到缓存中
  '/'.join(rdd.collect()) #第二次行动，重复使用缓存的rdd
  rdd.unpersist() #释放内存缓存的RDD
  ```
### RDD分区

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

```shell
2
5
1
```

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

### HBASE

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

## Spark SQL

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

- 创建DataFrame

  ```python
  spark.read.text('people.txt') #读取文本文件创建，本地file:///，hdfs://
  等价于spark.read.format('text').load('people.txt')
  spark.read.json('people.json')#读取json文件创建
  等价于spark.read.format('json').load('people.json')
  spark.read.parquet('people.parquet')#读取people.parquet文件创建
  等价于spark.read.format('parquet').load('people.parquet')
  ```

- 保存DataFrame

  ```python
  df.write.txt('people.txt') #保存为text目录
  等价于df.write.format('text').save('people.txt')
  df.write.json('people.json') #保存json目录
  等价于df.write.format('json').save('people.json')
  df.write.parquet('people.parquet')#保存parquet目录
  等价于df.write.format('parquet').save('people.parquet')
  ```

- 操作

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

  










