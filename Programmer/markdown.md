

# markdown教程

[toc]



# 一、流程图



```flow
st=>start
op=>operation: Operation
cond=>condition: Yes or No?
e=>end
st->op->cond
cond(yes)->e
cond(no)->op
```

# 二、代码块

选中代码右击插入代码块，选择代码语言即可

```html
<script>
function sum(a,b){
    return a+b
}
</script>
```

# 三、超链接

```shell
[文字](http链接地址)
```

[markdown笔记](http:)

# 四、图片

![图片]()

# 五、列表

语法：* 无序列表，数字. 有序列表（ *和.后面有个空格）如：

```shell
* 无序列表
1. 有序列表
嵌套列表快捷键：Ctrl+Enter键
```

* 无序列表
  * 嵌套列表
    1. 嵌套列表

# 六、标题

语法：# 标题，几个#几级标题（#后面有个空格），如：

```
### 三级标题
#### 四级标题
```

# 七、字体

```html
*倾斜*
**加粗**
***倾斜加粗***
~~删除线~~
```

*倾斜*
**加粗**
***倾斜加粗***
~~删除线~~

# 八、分割线

语法：不少于三个*

```
***
****
```

***
****
# 九、目录
[TOC]按回车键自动生成
