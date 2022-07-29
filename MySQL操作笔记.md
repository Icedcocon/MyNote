# 0 数据库常见概念

### 0.1 概念

**数据库：** 英文单词DataBase，简称DB。按照一定格式存储数据的一些文件的组合。 顾名思义：存储数据的仓库，实际上就是一堆文件。这些文件中存储了 具有特定格式的数据。

**数据库管理系统：** DataBaseManagement，简称DBMS。 数据库管理系统是专门用来管理数据库中数据的，数据库管理系统可以 对数据库当中的数据进行增删改查。

**常见的数据库管理系统：** MySQL、Oracle、MS SqlServer、DB2、sybase等....

**SQL：结构化查询语言** 程序员需要学习SQL语句，程序员通过编写SQL语句，然后DBMS负责执行SQL 语句，最终来完成数据库中数据的增删改查操作。

SQL是一套标准，程序员主要学习的就是SQL语句，这个SQL在mysql中可以使用， 同时在Oracle中也可以使用，在DB2中也可以使用。

**三者之间的关系？** DBMS--执行--> SQL --操作--> DB

先安装数据库管理系统MySQL，然后学习SQL语句怎么写，编写SQL语句之后，DBMS 对SQL语句进行执行，最终来完成数据库的数据管理。

### 0.2 SQL语句分类

**DQL：** 数据查询语言（凡是带有select关键字的都是查询语句） select...

**DML：** 数据操作语言（凡是对表当中的数据进行增删改的都是DML） insert、delete、update、insert 增、delete 删、update 改，​ 这个主要是操作表中的数据data。

**DDL：** 数据定义语言 凡是带有create、drop、alter的都是DDL。 DDL主要操作的是表的结构，不是表中的数据。 create：新建，等同于增； drop：删除； alter：修改。

**TCL：**  是事务控制语言 包括： 事务提交：commit; 事务回滚：rollback;

**DCL：** 是数据控制语言。 例如：授权grant、撤销权限revoke....

### 0.3 MYSQL中的数据类型

- **varchar(最长255)** **可变长度的字符串**，会根据实际的数据长度动态分配空间。
  
  - 优点：节省空间​ 
  
  - 缺点：需要动态分配空间，速度慢。

- **char(最长255)** **定长字符串**，分配固定长度的空间去存储数据。
  
  - 优点：不需要动态分配空间，速度快。
  
  - 缺点：使用不当可能会导致空间的浪费。

- **int(最长11)整型数字**。

- **bigint长整型数字**。

- **float单精度浮点型数据** 。

- **double双精度浮点型数据** 。

- **date短日期类型** 。

- **datetime长日期类型** 。

- **clob字符大对象** 最多可以存储4G的字符串。

- **blob二进制大对象** Binary Large OBject 
  
  - 专门用来存储图片、声音、视频等流媒体数据。 
  
  - 往BLOB类型的字段上插入数据的时需要使用IO流。

- t_movie 电影表（专门存储电影信息的）
  
  - 编号no(bigint) 、名字name(varchar) 、故事情节history(clob) 、上映日期、playtime(date)、时长time(double)、海报image(blob)、类型type(char)                            

### 0.4SQL脚本的执行

xxxx.sql这种文件被称为sql脚本文件。 sql脚本文件中编写了大量的sql语句。 我们执行sql脚本文件的时候，该文件中所有的sql语句会全部执行！ 批量的执行SQL语句，可以使用sql脚本文件。

# 1 数据库操作

### `CREATE DATABASE fryDemo DEFAULT CHARACTER SET = 'utf8mb4';`

**show databases;** 查看mysql中有哪些数据库

**use test;** 表示正在使用一个名字叫做test的数据库。

**create database db01;** 创建数据库

**show tables;** 查看某个数据库下有哪些表

**select version();** 查看mysql数据库的版本号

**select database();** 查看当前使用的是哪个数据库

**\c** 用来终止一条命令的输入。

# 2 建表操作

### 2.1 创建一个表create

- **建立新表**`create table 表名(字段名 属性 [,字段名 属性, ...]);`

- **从已存在列表创建一个表**`create table 新表名 select 字段名 from 旧表名;`

- **查看表结构**`desc 表名;`

```sql
-- 学号、姓名、年龄、性别、邮箱地址
 create table t_student(
     id int,
     name varchar(32),
     sex char(1),
     age int(3),
     email varchar(255)
 );

-- 从已存在的表创建一个表
create table `copy_student` 
select `name`,`sex`,`age`
from `t_student`;
```

### 2.2 删除一个表drop

- **删除表**`drop table 表名;`

```sql
drop table t_student; // 当这张表不存在的时候会报错！

drop table if exists t_student;// 如果这张表存在的话，删除
```

### 2.3 修改一个表alter

- **表增加一列**`alter table 表名 add 字段名;`

- **表删除一列**`alter table 表名 drop 字段名;`

- **表更改字段属性**`alter table 表名 modify/change 被修改字段名 [新字段名] [新属性];`

- **表更或设置改字段默认值**`alter table 表名 alter 字段名 set default 新值;`

- **表去除字段默认值**`alter table 表名 alter 字段名 drop default`

- **更改表名**`alter table 表名 rename to 新表名;`

```sql
alter table `t_student` 
add new_id int unsigned primary key auto_increment not null;
```

### 2.4 插入数据insert

- **插入单条数据**`insert into 表名(字段名1,字段名2,字段名3...) values(值1,值2,值3);`
- **插入多条数据**`insert into t_user(字段名1,字段名2) values(),(),(),();`

```sql
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
```

- insert语句没有给字段指定值的话，默认值是NULL。

### 2.5 修改数据update

- `update 表名 set 字段名1=值1,字段名2=值2,字段名3=值3... where 条件;`

- 没有条件限制会导致所有数据全部更新。

```sql
update t_user set name = 'jack', birth = '2000-10-11' where id = 2;
update t_user set name = 'jack', birth = '2000-10-11', create_time = now() where id = 2;
```

### 2.6 删除数据

**delete**语句（属于DML语句）

- 删除表中元组`delete from 表名 where 条件;`（没有条件会删除全部元组）
  
  - 表中的数据被删除了，但是这个数据在硬盘上的真实存储空间不会被释放
  
  - 这种删除缺点是：删除效率比较低。
  
  - 这种删除优点是：支持回滚，后悔了可以再恢复数据

**truncate**语句

- `truncate table 表名;` （属于DDL操作。）
  
  - 这种删除效率比较高，表被一次截断，物理删除。
  
  - 这种删除缺点：不支持回滚。
  
  - 这种删除优点：快速。

# 
