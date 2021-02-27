[下载安装](!https://hub.docker.com/editions/community/docker-ce-desktop-windows/)

思想：硬件共享，软件隔离

测试

```shell
docker run hello-world   测试是否成功  官方的测试镜像
docker info    查看信息
docker version   查看版本　
```

step1:阿里云

在[阿里云](!https://cr.console.aliyun.com/repository/cn-shenzhen/shanxidaxue/pytorch/details)创建地址，命名空间，镜像

step2:配置

linux平台pycharm中配置[环境](!https://tianchi.aliyun.com/competition/entrance/231759/tab/226)

step3:项目

创建项目文件夹，放Dockerfile、py文件、json文件以及run.sh

Dockerfile文件

```shell
# Base Images
## 从天池基础镜像构建
FROM registry.cn-shanghai.aliyuncs.com/tcc-public/python:3

## 把当前文件夹里的文件构建到镜像的根目录下
ADD . /

## 指定默认工作目录为根目录（需要把run.sh和生成的结果文件都放在该文件夹下，提交后才能运行）
WORKDIR /

## 镜像启动后统一执行 sh run.sh
CMD ["sh", "run.sh"]
```

run.sh文件

```shell
python hello_world.py
```

注意本地测试路径（一般在本地项目中）和镜像路径（在根目录）有所区别

step4:登录命令

```shell
sudo docker login --username=sunruirui1814@163.com registry.cn-shenzhen.aliyuncs.com
 #登录
docker pull registry.cn-shanghai.aliyuncs.com/tcc-public/python:3 #拉去python环境
docker pull registry.cn-shanghai.aliyuncs.com/tcc-public/pytorch:1.4-cuda10.1-py3 #拉取GPU环境
docker build -t registry.cn-shenzhen.aliyuncs.com/shanxidaxue/pytorch:1.0 . #版本号1.0可以更改
docker build -t registry.cn-shenzhen.aliyuncs.com/shanxidaxue/torch_cuda:1.0 .
docker run registry.cn-shenzhen.aliyuncs.com/shanxidaxue/pytorch:1.0 sh run.sh #CPU镜像
docker run registry.cn-shenzhen.aliyuncs.com/shanxidaxue/torch_cuda:1.0 sh run.sh
nvidia-docker run registry.cn-shenzhen.aliyuncs.com/shanxidaxue/torch_cuda:1.0 sh run.sh #GPU镜像
docker push registry.cn-shenzhen.aliyuncs.com/shanxidaxue/pytorch:1.0 #推送镜像
```

step5：提交结果

```shell
registry.cn-shenzhen.aliyuncs.com/shanxidaxue/pytorch:1.0 #镜像路径
登录的用户 #用户名
自己的密码 #密码
```

![image-20210209170406106](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20210209170406106.png)





```shell
docker run -it registry.cn-shanghai.aliyuncs.com/tcc-public/pytorch:1.4-cuda10.1-py3 /bin/bash #CPU
docker run --gpus all -it registry.cn-shanghai.aliyuncs.com/tcc-public/pytorch:1.4-cuda10.1-py3 /bin/bash
docker run -it -v /home/linux/桌面/tianchi_cuda/tcdata:/workspace/ registry.cn-shanghai.aliyuncs.com/tcc-public/pytorch:1.4-cud0.1-py3 /bin/bash #路径映射，本地绝对路径/home/linux/桌面/tianchi_cuda/tcdata映射到docker中/workspace
docker rmi -f id #删除镜像
docker rmi -f $(docker images | grep "none" | awk '{print $3}') #删除none镜像
```

