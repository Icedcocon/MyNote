```sql
-- #############################################################
-- 数据库常见概念
-- #############################################################

-- 1.概念
-- (1) 数据库(DataBase)：按照一定格式存储数据的一些文件的组合。
-- (2) 数据库管理系统(DataBaseManagement，DBMS)：管理数据库中数据
-- (3) 结构化查询语言(SQL)：一套操作数据库的标准
-- (4) 关系：DBMS--执行--> SQL --操作--> DB

-- 2.SQL语句分类
-- DQL：数据查询语言     select 查 ...
-- DML：数据操作语言     insert 增、delete 删、update 改 对数据
-- DDL：数据定义语言     create 增、drop   删、alter  改    对表结构
-- TCL：事务控制语言     commit 事务提交、rollback 事务回滚
-- DCL：数据控制语言     grant 授权、revoke 撤销权限

-- 3.数据类型
varchar        -- (最长255)    可变长度的字符串:会根据实际的数据长度动态分配空间。
char           -- (最长255)    定长字符串:分配固定长度的空间去存储数据。
int            -- (最长11)     整型数字
bigint         --             长整型数字
float          --             单精度浮点型数据
double         --             双精度浮点型数据
date           --             短日期类型
datetime       --             长日期类型
clob           --             字符大对象 最多可以存储4G的字符串。
blob           --             Binary Large OBject（图片、声音、视频等）  
t_movie        -- 电影表（专门存储电影信息的）
```

```sql
-- #############################################################
-- 数据库操作
-- #############################################################

-- 1.基本操作
create database demo default character set = 'utf8mb4';-- 新建 数据库
show databases;            -- 查看 mysql中有哪些数据库
use test;                  -- 使用 一个名字叫做test的数据库。
show tables;               -- 查看 当前数据库下有哪些表
select version();          -- 查看 mysql数据库的版本号
select database();         -- 查看 当前使用的是哪个数据库
\c                         -- 终止一条命令的输入。

-- 2.建表
-- (1) 建立新表          create table 表名(字段名 属性 [,字段名 属性, ...]);
-- (2) 从已存在列表创建   create table 新表名 select 字段名 from 旧表名;
-- (3) 查看表结构        desc 表名;
create table t_student(
     id int,
     name varchar(32),
     sex char(1),
     age int(3),
     email varchar(255)
); -- 建立新表
create table `copy_student` 
select `name`,`sex`,`age`
from `t_student`; -- 从已存在列表创

-- 3.删表
-- (1) 删除表            drop table 表名;
drop table t_student;             -- 当表不存在的时候报错
drop table if exists t_student;   -- 如果表存在则删除

-- 4.改表
-- (1) 表增加一列        alter table 表名 add 字段名;
-- (2) 表删除一列        alter table 表名 drop 字段名;
-- (3) 表更改字段属性    alter table 表名 modify/change 被修改字段名 [新字段名] [新属性];
-- (4) 表更或设置改字段默认值alter table 表名 alter 字段名 set default 新值;
-- (5) 表去除字段默认值   alter table 表名 alter 字段名 drop default
-- (6) 更改表名          alter table 表名 rename to 新表名;
alter table `t_student` 
add new_id int unsigned primary key auto_increment not null;

-- 4.增数据
-- (1) 插入单条数据 insert into 表名(字段名1,字段名2,...) values(值1,值2,...);
-- (2) 插入多条数据 insert into 表名(字段名1,字段名2) values(),(),(),();
-- (3) 修改数据插入 insert into 表名(字段名1,字段名2) select 新值,字段名2 from..;
-- 插入单条数据
insert into t_student(id,name,sex,age,email)
    values(1,'zhangsan','m',20,'zhangsan@123.com');
insert into t_student(id) values(3);
-- 省略字段名 必须按顺序
insert into t_student values(2, 'lisi', 'f', 20, 'lisi@123.com');
-- 插入多条数据
insert into t_user(id,name,birth,create_time) values
    (1,'zs','1980-10-11',now()), 
    (2,'lisi','1981-10-11',now()),
    (3,'wangwu','1982-10-11',now());

-- 5.改数据
-- (1) 修改数据    update 表名 set 字段名1=值1,字段名2=值2,字段名3=值3... where 条件
update t_user 
set name = 'jack', birth = '2000-10-11', create_time = now() 
where id = 2;

-- 6.删数据
-- (1) 删除表中元组（DML）可回滚效率低    delete from 表名 where 条件;
-- (2) 删除表中元组（DDL）无回滚效率高    truncate table 表名;
```

```sql
-- #############################################################
-- 单表查询
-- #############################################################

-- 基础条件查询
-- (0) 条件查询     select 字段1,字段2,字段3.... from 表名 where 条件;
-- (1) = 等于
select `name`,`sex` from t_student where `id`=2; 
-- (2) <>或!= 不等于
select `name`,`sex` from t_student where `id`<>2; 
-- (3) < 小于  <= 小于等于
select `name`,`sex` from t_student where `id`<2; 
-- (4) >大于  >= 大于等于
select `name`,`sex` from t_student where `id`>2; 
-- (5) between … and …. 两个值之间, 等同于 >= and <=
select `name`,`sex` from t_student where `id` between 2 and 4; 
select `name`,`sex` from t_student where `id`>=2 and `id`<=4; 
-- (6) is null 为 null（is not null 不为空）
select `name`,`sex` from t_student where `email` = null; 
select `name`,`sex` from t_student where `email` is not null; 
-- (7) and 且 or 或
select `name`,`sex` from t_student where `id`<2 or `id`>4; 
-- (8) in 包含，相当于多个 or （not in 不在这个范围中）
select `name`,`sex` from t_student where `id` in ('1','2','4','6'); 
-- (9) not 取非，主要用在 is 或 in 中
-- (10) like 模糊查询
select `name`,`sex` from t_student where `id` like '_';
-- (11) distinct 去重
select distinct name from t_student; -- distinct只能出现在**所有字段的最前方
select distinct name,sex from t_student; -- 两个字段联合起来去重

-- 排序
-- (1) asc默认升序**`select 字段 from 表名 order by 字段;`(ascend)
-- (2) desc指定降序**`select 字段 from 表名 order by 字段 desc;`(descend)
-- (3) 多个条件时，只有前面的条件都相等，才会启用后面的排序条件
select `name` from t_student order by `age`;
select `name` from t_student order by `age` desc;
select `name` from t_student order by `age` desc, `name` asc; -- 前等后排

-- 分页
-- (1) limit 分页查询             limit [startIndex], length;
-- (2) 每页pageSize条，第pageNo页：limit (pageNo - 1) * pageSize , pageSize
select name,sex from t_student order by id desc limit 5; -- 取id降序前5
select name,sex from t_student order by id desc limit 3,2; -- 取id 4-5

-- Union
-- (1) 
-- (2) union all 则将所有的结果全部显示出来，即便重复
```
