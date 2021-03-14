hadoop环境配置

[hdfs安装部署](https://www.cnblogs.com/youngchaolin/p/11992600.html )：

重点是免密登录从服务器节点，把主服务器密钥发给从服务器：在主服务器下运行 ssh-copy-id root@hadoop-slave1以及ssh-copy-id root@hadoop-slave2，在每个服务器都运行密钥发自己，自己也可以免密登录



```shell
#安全模式

hadoop dfsadmin -safemode get #查看安全状态

hadoop dfsadmin -safemode leave #离开安全模式

#关闭防火墙（查看web 50070及8080失败，需要关闭）:

systemctl stop firewalld.service*#停止firewall* 

systemctl disable firewalld.service*#禁止firewall开机启动*
```



hadoop基础操作

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

## 大数据时代

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



spark基本概念

![image-20210314173021016](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314173021016.png)

RDD：（多台机器内存分区，弹性：计算过程中动态调整分区数量），数据少可分布在一台机器内存，数据多可分布在多台机器内存中

- 只读的分布式分区（对象）集合
- RDD依赖关系：
  - 窄依赖：出度1，入度多 【map,filter,union,join】，可进行流水线优化
  - 宽依赖：出度多（一个父亲多个儿子）【groupby,join】，发生了shuffle（洗牌）操作（会写磁盘），可划分成多个阶段，不能进行流水线优化

![image-20210314183544657](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314183544657.png)

DAG:

![image-20210314173833456](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210314173833456.png)

```python
from pyspark import SparkConf,SparkContext
conf = SparkConf().setMaster("local").setAppName('My APP')
sc.stop()
sc = SparkContext(conf=conf)
logData = sc.textFile( "file:///root/tmp/student.txt",2).cache() #file://表示本地路径，后面跟绝对路径位置
numAs = logData.filter(lambda x:'1' in x).count()
numBs = logData.filter(lambda x:'C01' in x).count()
print(numAs,numBs)
```

