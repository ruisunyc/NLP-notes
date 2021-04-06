git教程

[TOC]

## 一、基本命令

```shell
git init #初始化Git，一般新建空文件夹，执行命令，会生成.git文件夹，之后命令行执行git操作
git add . #当前工作区更新添加到暂存区
git commit -m “介绍” #暂存区更到版本区
git reflog #查看版本
git checkout -b dev #创建新分支dev并进入分支
git rebase another master #master指向another,且HEAD指向master
git cherry-pick C2 C4 #抓取C2-C4分支放到HEAD节点下
git branch dev #在HEAD节点创建分支dev
git clone SSH地址#远程拷贝
git remote add origin “SSH地址” #添加远程地址到本地
git remote rm master #删除远程仓库master
git push --rebase #时间线推送更新到远程地址
git pull #拉去远程更新工作区，等价于fetch+merge
git fetch #获取远程更新，
git merge origin master #合并远程更新master到工作区master
git reset C1 #回撤版本到C1
git tag v1 HEAD #HEAD指向的节点为标签V1
```

***

## 二、实战场景

```shell
场景1(分支创建)
git checkout -b bugFix #创建分支并进入
git commit -m “分支修改”
git checkout master #切回主枝
git merge bugFix

场景2（分支合并）
git rebase master bugFix #bugFix分支合并到master中,且HEAD指向bugFix
git rebase bugFix side #把side分支合并到bugFix中,且HEAD指向side
git rebase side another  #把another分支合并到side中,且HEAD指向another
git rebase another master #master指向another,且HEAD指向master

场景3(版本回撤)
git reset HEAD^  本地回撤，HEAD回撤上一版本
git checkout pushed #切换分支
git revert HEAD 远程回撤

场景4(远程操作) 
git clone #无需init，克隆远程仓库到本地
git pull --rebase #获取远程更新到本地
git push #推送到远程更新

场景5(HEAD分离)：
git checkout HEAD^ #将HEAD指针后退一步，指向HEAD父节点
git branch -f bugFix HEAD~1 #将bugFix指针指向HEAD的父节点
git branch -f master C6 #将master指针指向hash值C6所在的节点

场景6(solo)
git reset --hard HEAD^ #回退版本(假设当前是C2,回退到C1)
git checkout -b feature C2 #在原先版本C2创建分支feature
git push #远程推送
```

***

## 三、在线练习

建议练习国人开发的一款闯关秘籍，[learnGitBranching](https://learngitbranching.js.org/?locale=zh_CN)

（查看隐藏答案，输入:show solution）

![image-20201209095020832](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20201209095020832.png)

##  四、环境配置

```python
$ git config --global user.name "Firstname Lastname" #设置使用Git 时的姓名
$ git config --global user.email "your_email@example.com" #设置使用Git时的邮箱地址
$ git config --global color.ui auto #将 color.ui 设置为 auto 界面好看
$ ssh-keygen -t rsa -C "your_email@example.com"# 设置ssh key，按回车即可
$ cat ~/.ssh/id_rsa.pub #查看公钥
$ ssh -T git@github.com #打开github，添加new ssh key，检验结果
```
## 五 mac安装
```python
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
 # mac下安装git和brew
```



