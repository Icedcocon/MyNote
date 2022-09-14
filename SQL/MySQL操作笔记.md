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

# 2 建表操作及增删改

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

# 3.单表查询

### 3.1基础条件查询

- **条件查询**`select 字段1,字段2,字段3.... from 表名 where 条件;`
1. **= 等于**

```sql
-- 查询薪资等于800的员工姓名和编号？
 select empno,ename from emp where sal = 800;
-- 查询SMITH的编号和薪资？
 select empno,sal from emp where ename = 'SMITH';
```

2. **<>或!= 不等于**

```sql
-- 查询薪资不等于800的员工姓名和编号？
 select empno,ename from emp where sal != 800;
 select empno,ename from emp where sal <> 800; // 小于号和大于号组成的不等号
```

3. **< 小于** **<= 小于等于**

```sql
-- 查询薪资小于等于3000的员工姓名和编号？
 select empno,ename,sal from emp where sal <= 3000;
```

4. **>大于  >= 大于等于**

```sql
-- 查询薪资大于等于3000的员工姓名和编号？
 select empno,ename,sal from emp where sal >= 3000;
```

5. **between … and …. 两个值之间, 等同于 >= and <=**

```sql
-- 查询薪资在2450和3000之间的员工信息？包括2450和3000
-- 第一种方式：>= and <= 
 select empno,ename,sal from emp where sal >= 2450 and sal <= 3000;
-- 第二种方式：between … and … 
 select empno,ename,sal from emp where sql between 2450 and 3000;
```

6. **is null 为 null（is not null 不为空）**

```sql
-- 查询哪些员工的津贴/补助为null？
 select empno,ename,sal,comm from emp where comm = null;
-- 查询哪些员工的津贴/补助不为null？
 select empno,ename,sal,comm from emp where comm is not null;
```

7. **and 且 or 或**

```sql
select * from emp where sal > 2500 and (deptno = 10 or deptno = 20);
-- and和or同时出现，and优先级较高。如果想让or先执行，需要加“小括号”。
```

8. **in 包含，相当于多个 or （not in 不在这个范围中）**

```sql
-- 查询工作岗位是MANAGER和SALESMAN的员工？
select empno,ename,job from emp where job = 'MANAGER' or job = 'SALESMAN';
select empno,ename,job from emp where job in('MANAGER', 'SALESMAN');
```

9. **not 取非，主要用在 is 或 in 中**

```sql
is null
is not null
in
not in
```

10. **like 模糊查询**

称为模糊查询，支持%或下划线匹配

- %匹配任意多个字符
- 下划线：任意一个字符。
- 查找含有通配符的字符串需要用'\'转义

```sql
-- 找出名字中含有O的？
 select ename from emp where ename like '%O%';
-- 找出名字中有“_”的？
 select name from t_student where name like '%_%'; //这样不行。
 select name from t_student where name like '%\_%'; // \转义字符。
```

11. **distinct 去重**
- 把查询结果去除重复记录【distinct】

- distinct只能出现在**所有字段的最前方**。

- distinct出现在job,deptno两个字段之前，表示**两个字段联合起来去重**。

```sql
 select distinct job from emp;
 select distinct job,deptno from emp;
```

### 3.2排序

- **asc默认升序**`select 字段 from 表名 order by 字段;`(ascend)

```sql
-- 查询所有员工薪资并排序？
 select ename,sal from emp order by sal; 
```

- **desc指定降序**`select 字段 from 表名 order by 字段 desc;`(descend)

```sql
 select ename,sal from emp order by sal desc;


-- 查询员工名字和薪资，要求按照薪资升序，如果薪资一样的话，再按照名字升序排列。
 select ename,sal from emp order by sal asc, ename asc; 
-- sal在前，起主导，只有sal相等的时候，才会考虑启用ename排序。
```

### 3.3分页

- **limit 分页查询**`limit startIndex, length;`
  
  - 作用：将查询结果集的一部分取出来。通常使用在分页查询当中。
  
  - 起始**下标从0开始**。
  
  - 缺省用法：`limit 5;` 取前5.

```sql
-- 按照薪资降序，取出排名在前5名的员工？
select ename,sal from emp order by sal desc limit 5;
-- limit在order by之后执行


-- 取出工资排名在[3-5]名的员工？
select ename,sal from emp order by sal desc limit 2, 3;
-- 2表示起始位置从下标2开始，就是第三条记录。3表示长度。
```

- 每页显示3条记录
  
  - 第1页：`limit 0,3 [0 1 2]`
  - 第2页：`limit 3,3 [3 4 5]`
  - 第3页：`limit 6,3 [6 7 8]`

- 每页显示pageSize条记录
  
  - **第pageNo页：`limit (pageNo - 1) * pageSize , pageSize`**

# 4.函数

### 4.1单行处理函数

- 单行处理函数特点：一个输入对应一个输出。

- 多行处理函数特点：多个输入对应一个输出。
1. lower/upper 转换小写/大写

```sql
 select lower(ename) as ename from emp;
```

2. substr 取子串`substr( 被截取的字符串, 起始下标, 截取的长度);`

```sql
select substr(ename, 1, 1) as ename from emp;
-- 注意：起始下标从1开始，没有0.

-- 找出员工名字第一个字母是A的员工信息？
-- 第一种方式：模糊查询
 select ename from emp where ename like 'A%';
-- 第二种方式：substr函数
 select ename from emp where substr(ename,1,1) = 'A';
```

3. concat函数进行字符串的拼接

```sql
 select concat(empno,ename) from emp;
```

4. length 取长度

```sql
 select length(ename) enamelength from emp;
```

5. trim 去空格

```sql
 select * from emp where ename = '  KING';
```

str_to_date 将字符串转换成日期
date_format 格式化日期
format 设置千分位
round 四舍五入

        select 字段 from 表名;
        select ename from emp;
        select 'abc' from emp; // select后面直接跟“字面量/字面值”
        mysql> select 'abc' as bieming from emp;
        select round(1236.567, 1) as result from emp; //保留1个小数
        select round(1236.567, 2) as result from emp; //保留2个小数
        select round(1236.567, -1) as result from emp; // 保留到十位。

rand() 生成随机数

        mysql> select round(rand()*100,0) from emp; // 100以内的随机数

ifnull 可以将 null 转换成一个具体值

        ifnull是空处理函数。专门处理空的。
        在所有数据库当中，只要有NULL参与的数学运算，最终结果就是NULL。
        mysql> select ename, sal + comm as salcomm from emp;

### 4.2分组函数

- 多行处理函数的特点：输入多行，最终输出一行。
  - count 计数
  - sum 求和
  - avg 平均值
  - max 最大值
  - min 最小值
- 注意： 分组函数在使用的时候必须先进行分组，然后才能用。 如果你没有对数据进行分组，整张表默认为一组。

找出最高工资？
        mysql> select max(sal) from emp;
找出最低工资？
        mysql> select min(sal) from emp;
计算工资和：
        mysql> select sum(sal) from emp;
计算平均工资：
        mysql> select avg(sal) from emp;
计算员工数量？
        mysql> select count(ename) from emp;

**分组函数在使用的时候需要注意哪些？**

- 第一点：分组函数自动忽略NULL，你不需要提前对NULL进行处理。
- 第二点：分组函数中count(*)和count(具体字段)有什么区别？*
  - count(具体字段)：表示统计该字段下所有不为NULL的元素的总数。
  - count(*)：统计表当中的总行数。（只要有一行数据count则++） 因为每一行记录不可能都为NULL，一行数据中有一列不为NULL，则这行数据就是有效的。
- 第三点：分组函数不能够直接使用在where子句中。 找出比最低工资高的员工信息。 select ename,sal from emp where sal > min(sal); 表面上没问题，运行一下？ ERROR 1111 (HY000): Invalid use of group function
