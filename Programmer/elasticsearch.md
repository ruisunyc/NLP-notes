[TOC]

## es 安装

* 安装docker-compose

  ```shell
  源码下载
  python setup.py install #安装
  chmod +x /usr/local/bin/docker-compose #权限
  ```

* 启动docker

  ```shell
  systemctl status docker.service #检查状态
  service docker start #启动
  systemctl enable docker.service #开机启动
  ```

* 安装es

  ```shell
  mkdir /opt/docker-es #创建目录
  vim /opt/docker-compose.yml #创建并编辑安装文件
  docker-compose up -d #安装es
  ```

  也可复制配置到docker-compose.yml，并上传文件到docker-es目录下

```yaml
version: '2'
services:
  elasticsearch:
    container_name: elasticsearch
    image: daocloud.io/library/elasticsearch:6.5.4
    ports:
      - "9200:9200"
    environment:
      - "ES_JAVA_OPTS=-Xms64m -Xmx128m"
      - "discovery.type=single-node"
      - "COMPOSE_PROJECT_NAME=elasticsearch-server"
    restart: always

  kibana:
    container_name: kibana
    image: daocloud.io/library/kibana:6.5.4
    ports:
      - "5601:5601"
    restart: always
    environment:
      - ELASTICSEARCH_HOSTS=http://192.168.1.185:9200
```

* 安装分词器

  ``` shell
  docker ps #查看docker标识
  docker exec -it 807 bash #807即es标识
  ./bin/elasticsearch-plugin install https://github.91chifun.workers.dev//https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v6.5.4/elasticsearch-analysis-ik-6.5.4.zip #在线安装分词器
  ```

* 重启并验证es

  ```shell
  exit
  docker restart 807
  http://192.168.1.185:9200
  http://192.168.1.185:5601
  ```

* 测试分词
  ![image-20201203174726276](/image/es.png)

* 安装注意事项
  1. [docker仓库](http://hub.daocloud.io)
  2. es,kibana,ik版本要一致，如都为6.5.4

## es 操作

```shell
索引->type->doc->field #es结构
(库，表，行，字段) #msyql结构
```



[es教程](https://www.cnblogs.com/Neeo/articles/10615615.html)

