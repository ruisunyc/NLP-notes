+ ### Django教程

  ```shell
  python -m venv ll_env #创建虚拟环境
  source ll_env/bin/activate #激活虚拟环境
  pip install django==2.2.0 #安装django
  django-admin startproject learning_log . #在当前目录新建Django工程learing_log
  python manage.py migrate #数据库迁移，sqlite
  python manage.py runserver #启动服务，打开网址
  python manage.py startapp learning_logs #创建APP
python manage.py makemigrations learning_logs #Model迁移数据库
  python manage.py migrate #执行迁移
  ```
  
  ![image-20201225190202327](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20201225190202327.png)



参考文献

1. python镜像源

   ```shell
   pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -U tensorflow==2.0.0
   pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -U tensorflow==1.6.0
   pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -U PyMySQL==0.8.0
   pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -U DBUtils==1.2
   pip install  -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -U tensorboardX
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -U pytorch==1.1.0
   pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -U tqdm
   pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -U sklearn
   pip install cupy-cuda100==7.0 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
   ```

2. [Github加速方法](https://www.tianqiweiqi.com/github-open.html)

2. [python变量可视化]( http://pythontutor.com/live.html#mode=edit)

4. [python环境](https://www.jianshu.com/p/e191f9dc1186)

   ```shell
   #针对一台刚装好的centos7，环境搭建基本步骤,拷贝虚拟环境源码安装
   yum install vim
   yum install -y gcc
   yum install unzip
   ```

   notebook 自动补全

   ```shell
   pip install jupyter_contrib_nbextensions -i https://pypi.tuna.tsinghua.edu.cn/simple
   jupyter nbextensions_configurator enable --user
   jupyter contrib nbextension install --user --skip-running-check 
   ```

5. pycharm添加镜像:

   ```python
   https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
   https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
   defaults
   ```

6. tensor/numpy/list

   ```python
   1.1 list 转 numpy
   
   ndarray = np.array(list)
   
   1.2 numpy 转 list
   
   list = ndarray.tolist()
   
   2.1 list 转 torch.Tensor
   
   tensor=torch.Tensor(list)
   
   2.2 torch.Tensor 转 list
   
   先转numpy，后转list
   
   list = tensor.numpy().tolist()
   
   3.1 torch.Tensor 转 numpy
   
   ndarray = tensor.numpy()
   
   *gpu上的tensor不能直接转为numpy
   
   ndarray = tensor.cpu().numpy()
   
   3.2 numpy 转 torch.Tensor
   tensor = torch.from_numpy(ndarray)
   
   ```

   pytorch 可视化
   
   ```shell
   tensorboard --logdir log
   ```
   
   单例模式
   
   ```python
   class Singleton:
       _lock = threading.Lock()
       def __new__(cls,*arg,**kwargs):
           if not hasattr(cls,'_instance'):
               with Singleton._lock:
                   if not hasattr(cls,'_instance'):
                       Singleton._instance = super().__new__(cls)
           return Singleton._instance
   def task(arg):
       print(Singleton())
   for i in range(10):
       t = threading.Thread(target = task,args=[i,])
       t.start()
   ```
   
   装饰器
   
   ```python
   import os
   import time
   import logging
   
   logger = logging.getLogger()
   logger.setLevel(20)
   
   execute_time = time.strftime("%Y_%m_%d")
   
   filepath = '/%s_log.log' % execute_time
   file_dir_path = os.path.dirname(filepath)
   
   if not os.path.exists(file_dir_path):
       os.makedirs(file_dir_path)
   file_handler = logging.FileHandler(filepath, encoding='utf-8')
   formatter = logging.Formatter("%(asctime)s - 【%(levelname)s】 - %(message)s")
   file_handler.setFormatter(formatter)
   logger.addHandler(file_handler)
   
   
   def log_decorator(message=None):
       def log_fun(func):
           def execute_fun(*args, **kwargs):
               try:
                   if len(args) == 0 and len(kwargs) == 0:
                       params_data = None
                   else:
                       params_data = args if args else kwargs if kwargs else None
                       if str(params_data[0]).find("object") != -1:
                           params_data = params_data[1:]
                       if len(params_data) == 0:
                           params_data = None
                   if params_data is not None:
                       params_info = "，Execute Arguments：【{0}】".format(str(params_data))
                   else:
                       params_info = ''
                   execute_result = func(*args, **kwargs)
                   logger.info("【{0}】-".format(func.__name__) + message + "PASS" + params_info)
                   return execute_result
               except Exception as e:
                   logger.error("【{0}】-".format(func.__name__) + message + "Fail" + params_info + "\n\t" + str(e) + "\n", exc_info=1)
                   raise e
           return execute_fun
       return log_fun
   ```
   
   



