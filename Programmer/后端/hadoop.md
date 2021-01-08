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

