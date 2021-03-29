### 一、常用SQL优化

1、原则一：**避免** **SELECT \***，而使用字段名

原则二：使用order by 或group by 优化速度

2、一条语句结果时，使用limit 1，例如：

```mysql
table_out = '20180519_关键词分类表'    
sql_selectcmd = 'SELECT OBJECT_ID FROM ' +table_out+' ORDER BY OBJECT_ID DESC LIMIT 1'
```

3、对检索的字段使用**索引**，一般唯一主键添加索引，或者为**搜索字段建索引，** 性能至少快4倍。

```mysql
-- 主键索引
ALTER TABLE `table_name` ADD PRIMARY KEY ( `column` ) 
-- 全文索引
ALTER TABLE `dn_location3` ADD PRIMARY KEY(OBJECT_ID)
-- 唯一索引
ALTER TABLE `20180519_关键词分类表` ADD UNIQUE index_keys(OBJECT_ID)
-- 下表多列添加索引
ALTER TABLE `20180519_关键词分类表` ADD INDEX index_keys(OBJECT_ID,KEYWORD);
-- 显示索引语句
show index from `20180519_关键词分类表`
-- 删除建立的索引
DROP index index_keys on `20180519_关键词分类表`
```

4、使用 ENUM 而不是 VARCHAR

Enum是**枚举**类型，比如“性别”，“国家”，“民族”，“状态”或“部门”，这些字段的取值是有限而且固定的，那么应该使用 ENUM 而不是 VARCHAR

5、多表查询时，使用exists字段，且建立索引

```mysql
update t
set key1 = null, value1 = null
where exists (select 1 from black_list where name = key1);
```

6、分批执行

无论是插入还是更新，最好多条一起执行。Mysql多条执行函数为：

executeMany(sql, params),其中params是元祖列表

```mysql
cur.executemany("UPDATE Writers SET Name = %s，Name1 = %s WHERE Id = %s ",[("new_value" , "3"),("new_value" , "6")])
```

7、分页优化

```mysql
-- 主键索引
-- 添加order by object_id,时间: 4.276s
SELECT OBJECT_ID,PROJECT_NAME,CONTENT,PROVINCE_ID,CITY_ID,COUNTY_ID 
FROM t_bidding_info where OBJECT_ID >= 11476872 and OBJECT_ID<=22011654 
and TYPE = 1
ORDER BY OBJECT_ID
LIMIT 200000,20
-- 时间: 469.195s
SELECT OBJECT_ID,PROJECT_NAME,CONTENT,PROVINCE_ID,CITY_ID,COUNTY_ID 
FROM t_bidding_info where OBJECT_ID >= 11476872 and OBJECT_ID<=22011654 
and TYPE = 1
LIMIT 200000,20
-- 查询多个字段时，查询出最大偏移量的uid,再进行分页
-- 优化前  147.870s
SELECT OBJECT_ID,PROJECT_NAME,CONTENT,PROVINCE_ID,CITY_ID,COUNTY_ID 
FROM t_bidding_info 
where OBJECT_ID >= 11476872 and OBJECT_ID<=22011654 
and TYPE = 1
ORDER BY OBJECT_ID 
LIMIT 2000000,8
-- 优化后  0.865s
SELECT OBJECT_ID,PROJECT_NAME,CONTENT,PROVINCE_ID,CITY_ID,COUNTY_ID 
FROM t_bidding_info 
where OBJECT_ID>=(SELECT OBJECT_ID from t_bidding_info where OBJECT_ID >= 11476872 and OBJECT_ID<=22011654 
and TYPE = 1 ORDER BY OBJECT_ID LIMIT 2000000,1)
and TYPE = 1 and OBJECT_ID<=22011654
ORDER BY OBJECT_ID 
LIMIT 8
-- 使用where条件object_ID+x代替limit x,y中的x
-- 使用where id between x and y
```

8、mysql 自动获取当前时间：

在数据表中，要记录每条数据是什么时候创建（修改）的，不需要应用程序去特意记录，而由数据数据库获取当前时间自动记录创建（修改）时间

```mysql
-- 新增创建时间字段
ALTER TABLE  20181203_tender_format_500
add COLUMN  `CREATE_TIME` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间' 
-- 新增更新时间字段
ALTER TABLE 20181205_tender_format
ADD COLUMN `UPDATE_TIME` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间' 
```



### 二、存储优化

数据库引擎为Innodb， 使用与业务无关的自增字段做主键（减少索引频繁插入移动数据）

B树(m阶平衡查找树)

1. 最少有$\lceil m/2 \rceil-1$个关键字,最多有$m-1$个关键字，根节点可以一个关键字

2. 每个节点关键字是排序的，左子树关键字小于它，右子树关键字大于它

3. 所有叶子节点在同一层，根节点到每个节点高度相同

插入操作：先在叶子节点找到插入位置，超过最大范围m-1取中间位置向上分裂（缺点浪费空间）

删除操作：
非叶子节点删除，从后继借关键字替换，若删除后继后关键字个数小于最小范围$\lceil m/2 \rceil-1$则从兄弟借关键字替换借的那个关键字，借的那个关键字下移

叶子节点删除，不满足条件从兄弟借，若兄弟借不了，从父亲借，之后叶子节点要合并调整，若父亲也不满足则继续让父亲的兄弟（从伯伯们）借，还不满足，再从爷爷借

B+树

1. 叶子节点多了前驱和后继指针
2. 数据存在叶子节点，而非叶子节点只存放指针

删除叶子节点从兄弟借，不满足则合并

插入还是不满足条件则向上分裂，最左端比当前小，中间及以后大于等于父节点指针

### 三、参考文献

[知乎](!https://www.zhihu.com/question/264861637/answer/286272651)

[博客](!http://blog.codinglabs.org/articles/theory-of-mysql-index.html)
