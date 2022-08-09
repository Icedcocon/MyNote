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

### 3.4Union

- 将两个 select 语句的结果作为一个整体显示出来。

- 两者区别：
  
  - union 会自动压缩多个结果集合中的重复结果
  
  - union all 则将所有的结果全部显示出来，即便重复。

- union (all)对两个结果集进行并集操作，同时进行默认规则的排序

```sql
# ====================== OR ===========================
mysql>  select ename,job from emp where job = 'SALESMAN' or job = 'MANAGER';
+--------+----------+
| ename  | job      |
+--------+----------+
| ALLEN  | SALESMAN |
| WARD   | SALESMAN |
| JONES  | MANAGER  |
| MARTIN | SALESMAN |
| BLAKE  | MANAGER  |
| CLARK  | MANAGER  |
| TURNER | SALESMAN |
+--------+----------+
# ====================== IN ===========================
mysql> select ename,job from emp where job in('MANAGER','SALESMAN');
+--------+----------+
| ename  | job      |
+--------+----------+
| ALLEN  | SALESMAN |
| WARD   | SALESMAN |
| JONES  | MANAGER  |
| MARTIN | SALESMAN |
| BLAKE  | MANAGER  |
| CLARK  | MANAGER  |
| TURNER | SALESMAN |
+--------+----------+
# ====================== UNION ===========================
select ename,job from emp where job = 'MANAGER'
union
select ename,job from emp where job = 'SALESMAN';
+--------+----------+
| ename  | job      |
+--------+----------+
| JONES  | MANAGER  |
| BLAKE  | MANAGER  |
| CLARK  | MANAGER  |
| ALLEN  | SALESMAN |
| WARD   | SALESMAN |
| MARTIN | SALESMAN |
| TURNER | SALESMAN |
+--------+----------+


```

- UNION 和 UNION ALL 内部的 SELECT 语句必须拥有**相同数量的字段**。

- 如果UNION前后的SELECT语句中字段顺序不同，**结果字段的顺序以union 前面的表字段顺序为准**。

# 4.函数

### 4.1单行处理函数

- 单行处理函数特点：一个输入对应一个输出。

- 多行处理函数特点：多个输入对应一个输出。
1. **lower/upper** 转换小写/大写

```sql
 select lower(ename) as ename from emp;
```

2. **substr** 取子串`substr( 被截取的字符串, 起始下标, 截取的长度);`

```sql
select substr(ename, 1, 1) as ename from emp;
-- 注意：起始下标从1开始，没有0.

-- 找出员工名字第一个字母是A的员工信息？
-- 第一种方式：模糊查询
 select ename from emp where ename like 'A%';
-- 第二种方式：substr函数
 select ename from emp where substr(ename,1,1) = 'A';
```

3. **concat** 函数进行字符串的拼接

```sql
 select concat(empno,ename) from emp;
```

4. **length** 取长度

```sql
 select length(ename) enamelength from emp;
```

5. **trim** 去空格

```sql
 select trim(ename),trim(empno) from emp where ename = '  KING';
```

6. **str_to_date** 将字符串转换成日期

```sql
SELECT STR_TO_DATE('2017-01-06 10:20:30','%Y-%m-%d %H:%i:%s') AS result1;
SELECT STR_TO_DATE('2017-01-06 10:20:30','%Y-%m-%d') AS result2;
```

7. **date_format** 用于以不同的格式显示时间数据，`DATE_FORMAT(*date*,*format*)`
   
   | 格式  | 描述                           |
   | --- | ---------------------------- |
   | %a  | 缩写星期名                        |
   | %b  | 缩写月名                         |
   | %c  | 月，数值                         |
   | %D  | 带有英文前缀的月中的天                  |
   | %d  | 月的天，数值(00-31)                |
   | %e  | 月的天，数值(0-31)                 |
   | %f  | 微秒                           |
   | %H  | 小时 (00-23)                   |
   | %h  | 小时 (01-12)                   |
   | %I  | 小时 (01-12)                   |
   | %i  | 分钟，数值(00-59)                 |
   | %j  | 年的天 (001-366)                |
   | %k  | 小时 (0-23)                    |
   | %l  | 小时 (1-12)                    |
   | %M  | 月名                           |
   | %m  | 月，数值(00-12)                  |
   | %p  | AM 或 PM                      |
   | %r  | 时间，12-小时（hh:mm:ss AM 或 PM）   |
   | %S  | 秒(00-59)                     |
   | %s  | 秒(00-59)                     |
   | %T  | 时间, 24-小时 (hh:mm:ss)         |
   | %U  | 周 (00-53) 星期日是一周的第一天         |
   | %u  | 周 (00-53) 星期一是一周的第一天         |
   | %V  | 周 (01-53) 星期日是一周的第一天，与 %X 使用 |
   | %v  | 周 (01-53) 星期一是一周的第一天，与 %x 使用 |
   | %W  | 星期名                          |
   | %w  | 周的天 （0=星期日, 6=星期六）           |
   | %X  | 年，其中的星期日是周的第一天，4 位，与 %V 使用   |
   | %x  | 年，其中的星期一是周的第一天，4 位，与 %v 使用   |
   | %Y  | 年，4 位                        |
   | %y  | 年，2 位                        |

```sql
DATE_FORMAT(NOW(),'%b %d %Y %h:%i %p')
DATE_FORMAT(NOW(),'%m-%d-%Y')
```

8. **format** 设置千分位,`FOMRAT(N,D,locale);`
- FORMAT函数接受三个参数：
  
  - N 是要格式化的数字。
  
  - D 是要舍入的小数位数。
  
  - locale 是一个可选参数，用于确定千个分隔符和分隔符之间的分组。如果省略locale操作符，MySQL将默认使用en_US。

```sql
SELECT FORMAT(14500.2018, 2); -- 保留两位小数
SELECT FORMAT(12500.2015, 0); -- 不保留小数


SELECT 
    productname,
    CONCAT('￥', FORMAT(quantityInStock * buyPrice, 2)) stock_value
FROM
    products;
```

9. **round** 四舍五入

```sql
 select round(1236.567, 1) as result from emp; //保留1个小数
 select round(1236.567, 2) as result from emp; //保留2个小数
 select round(1236.567, -1) as result from emp; // 保留到十位。
```

10. **rand**  生成随机数

```sql
 select round(rand()*100,0) from emp; // 100以内的随机数
```

11. **ifnull** 可以将 null 转换成一个具体值，`IFNULL(expression_1,expression_2);`
- 如果expression_1不为NULL，则IFNULL函数返回expression_1; 否则返回expression_2的结果。

```sql
 select contactname,IFNULL(bizphone,homephone) phone from contacts;
```

12. **datediff** 返回`startdate`和`enddate`间的间隔的天数（MySQL）。**`DATEDIFF(datepart,startdate,enddate)`（其他）**
    
    **`DATEDIFF(date1,date2)`（MySQL）**
    
    - startdate和enddate参数是合法的日期表达式。
    
    - datepart参数可以是下列的值：

| **设置** | **描述** |
|:------ | ------ |
| yyyy   | 年      |
| q      | 季度     |
| m      | 月      |
| y      | 一年的日数  |
| d      | 日      |
| w      | 一周的日数  |
| ww     | 周      |
| h      | 小时     |
| n      | 分钟     |
| s      | 秒      |

```sql
SELECT DATEDIFF('2008-11-30','2008-11-29') AS DiffDate
--      1
SELECT DATEDIFF('2008-11-29','2008-11-30') AS DiffDate
--     -1
```

### 4.2分组函数

- 多行处理函数的特点：输入多行，最终输出一行。
  - count 计数
  - sum 求和
  - avg 平均值
  - max 最大值
  - min 最小值
- 注意： 分组函数在使用的时候必须先进行分组，然后才能用。 如果没有进行分组，默认整张表为一组。

```sql
-- 找出最高工资？
 select max(sal) from emp;
-- 找出最低工资？
 select min(sal) from emp;
-- 计算工资和：
 select sum(sal) from emp;
-- 计算平均工资：
 select avg(sal) from emp;
-- 计算员工数量？
 select count(ename) from emp;
```

**分组函数在使用的时候需要注意哪些？**

- 分组函数自动忽略NULL，你不需要提前对NULL进行处理。
- 分组函数中`count(*)`和`count(字段)`有什么区别？\*
  - `count(字段)`：表示统计该字段下所有不为NULL的元素的总数。
  - `count(*)`：统计表当中的总行数。
- 分组函数不能够直接使用在where子句中。 找出比最低工资高的员工信息。 如：`select ename,sal from emp where sal > min(sal);`

# 5.分组查询

### 5.1 group by

```sql
-- 找出每个工作岗位的工资和？
-- 实现思路：按照工作岗位分组，然后对工资求和。
select job,sum(sal) from emp group by job;
```

- 执行顺序：
  
  - 从emp表中查询数据。
  
  - 根据job字段进行分组。
  
  - 然后对每一组的数据计算`sum(sal)`

- 在一条select语句当中，如果有group by语句的话，select后面只能跟：
  
  - **参加分组的字段**
  
  - **分组函数**

```sql
-- 找出每个部门的最高薪资
-- 实现思路:按照部门编号分组，求每一组的最大值。
 select deptno,max(sal) from emp group by deptno;
```

### 5.2 联合分组

```sql
-- 找出“每个部门，不同工作岗位”的最高薪资？
-- 两个字段联合成1个字段看。（两个字段联合分组）
 select deptno,job,max(sal) from emp group by deptno,job;
```

### 5.3having

- 使用having可以对分完组之后的数据进一步过滤。

- having不能单独使用，having不能代替where，having必须和group by联合使用。

```sql
-- 找出每个部门平均薪资，要求显示平均薪资高于2500的。
select deptno,avg(sal) from emp group by deptno having avg(sal) > 2500;
```

- where和having，优先选择where，where实在完成不了了，再选择having。

### 5.4总结sql执行顺序

- 关键字顺序
  
  - **select --> from --> where --> group by --> having --> order by**

- 执行顺序
1. 从某张表中查询数据。                                （from）
2. 先经过where条件筛选出有价值的数据。 （where）
3. 对这些有价值的数据进行分组。                （group by）
4. 分组之后可以使用having继续筛选。        （having）
5. select查询出来。                                        （select）
6. 最后排序输出。                                           （order by）

```sql
-- 找出每个岗位的平均薪资，要求显示平均薪资大于1500的，除MANAGER岗位之外，
-- 要求按照平均薪资降序排。
select job, avg(sal) as avgsal
from emp
where job <> 'MANAGER'
group by job
having avg(sal) > 1500
order by avgsal desc;
```

## 6.连表查询

- 从一张表中单独查询，称为单表查询

- 跨表查询，多张表联合起来查询数据，被称为连接查询。

```sql
-- emp表和dept表联合起来查询数据，从emp表中取员工名字，从dept表中取部门名字。
 select ename,dname from emp, dept;
```

- 当两张表进行连接查询，没有任何条件限制的时候，最终查询结果条数，是两张表条数的乘积，即笛卡尔积。

### 6.1内连接-等值连接

```sql
-- 查询每个员工所在部门名称，显示员工名和部门名？

-- SQL92语法：
 select e.ename,d.dname from emp e, dept d where e.deptno = d.deptno;
-- sql92的缺点：结构不清晰，表的连接条件，和后期进一步筛选的条件，都放到了where后面。

-- SQL99语法：
-- inner可以省略
 select e.ename,d.dname from emp e inner join dept d on e.deptno = d.deptno;
-- sql99优点：连接的条件是独立的，连接后进一步筛选，可以添加where
```

### 6.2内连接-非等值连接

```sql
-- 找出每个员工的薪资等级，要求显示员工名、薪资、薪资等级？
select e.ename, e.sal, s.grade 
from emp e join salgrade s 
on e.sal between s.losal and s.hisal; 
```

### 6.3内连接-自连接

```sql
-- 查询员工的上级领导，要求显示员工名和对应的领导名？
-- 一张表看成两张表。
select a.ename as '员工名', b.ename as '领导名'
from emp a
join emp b
on a.mgr = b.empno;
```

### 6.4外连接

- 区别

<img title="" src="https://img2020.cnblogs.com/blog/2478745/202109/2478745-20210920231243717-246783134.png" alt="" data-align="center" width="282">

| 操作         | 描述                    |
| ---------- | --------------------- |
| inner join | 如果表中至少有一个匹配，就返回值      |
| left join  | 会从左表中返回所有的值，即使右表中没有匹配 |
| right join | 会从右表中返回所有的值，即使左表中没有匹配 |

- 例子

```sql
-- outer可省略。
select e.ename,d.dname
from emp e 
right outer join dept d
on e.deptno = d.deptno;

select e.ename,d.dname 
from dept d 
left outer join emp e
on e.deptno = d.deptno;
```

### 6.5多表连接

- **多张表的连接语法：**

```sql
-- 语法：
    select     ...
    from       a
    join       b
    on         a和b的连接条件
    join       c
    on         a和c的连接条件
    right join d
    on         a和d的连接条件
```

```sql
-- 找出每个员工的部门名称以及工资等级，要求显示员工名、部门名、薪资、薪资等级？
select e.ename,e.sal,d.dname,s.grade
from emp e
join dept d
on e.deptno = d.deptno
join salgrade s 
on e.sal between s.losal and s.hisal;


-- 找出每个员工的部门名称以及工资等级，还有上级领导，要求显示员工名、领导名、部门名、薪资、薪资等级？**
select e.ename,e.sal,d.dname,s.grade,l.ename
from emp e
join dept d
on e.deptno = d.deptno
join salgrade s
on e.sal between s.losal and s.hisal
left join emp l
on e.mgr = l.empno;
```

## 7.子查询

- select语句中嵌套select语句，被嵌套的select语句称为子查询。

- 子查询**可以出现在 select、from、where 后面**。

### 7.1where子句中的子查询

```sql
-- 找出比最低工资高的员工姓名和工资？
 select ename,sal from emp where sal > (select min(sal) from emp);
```

### 7.2from子句中的子查询

- from后面的子查询，可以将子查询的查询结果当做一张临时表。

```sql
-- 找出每个岗位的平均工资的薪资等级。
select t.*, s.grade
from (select job,avg(sal) as avgsal from emp group by job) t
join salgrade s
on t.avgsal between s.losal and s.hisal;
```

## 8.约束

### 8.1约束类型

- 非空约束：**not null**
- 唯一性约束: **unique**
- 主键约束: **primary key** （简称PK）
- 外键约束：**foreign key**（简称FK）
- 检查约束：check（mysql不支持，oracle支持）**

### 8.2not null

- 非空约束not null约束的字段不能为NULL。

```sql
drop table if exists t_vip;
create table t_vip(
    id int,
    name varchar(255) not null // not null只有列级约束，没有表级约束！
    );
insert into t_vip(id,name) values(1,'zhangsan');
insert into t_vip(id) values(3);
-- ERROR 1364 (HY000): Field 'name' doesn't have a default value
```

### 8.3unique

- 唯一性约束unique约束的字段不能重复，但是**可以为NULL**。

```sql
drop table if exists t_vip;
create table t_vip(
    id int,
    name varchar(255) unique,
    email varchar(255)
);
insert into t_vip(id,name,email) values(2,'lisi','lisi@123.com');
insert into t_vip(id,name,email) values(3,'wangwu','wangwu@123.com');
insert into t_vip(id,name,email) values(4,'wangwu','wangwu@sina.com');
-- ERROR 1062 (23000): Duplicate entry 'wangwu' for key 'name'
insert into t_vip(id) values(4);
insert into t_vip(id) values(5);
```

#### 8.3.1联合唯一

```sql
-- name和email两个字段联合起来具有唯一性
drop table if exists t_vip;
create table t_vip(
    id int,
    name varchar(255),
    email varchar(255),
    unique(name,email) // 约束没有添加在列的后面，这种约束被称为表级约束。
    );
insert into t_vip(id,name,email) values(1,'zhangsan','zhangsan@123.com');
insert into t_vip(id,name,email) values(2,'zhangsan','zhangsan@sina.com');
-- name和email两个字段联合起来唯一

insert into t_vip(id,name,email) values(3,'zhangsan','zhangsan@sina.com');
-- ERROR 1062 (23000): Duplicate entry 'zhangsan-zhangsan@sina.com' for key 'name'
```

- 在mysql当中，如果一个字段同时被not null和unique约束的话，该字段自动变成主键字段。（注意：oracle中不是）

### 8.4primary key

- 主键值是每一行记录的唯一标识。

- 主键的特征：not null + unique（主键值不能是NULL，同时也不能重复！）

```sql
drop table if exists t_vip;
-- 1个字段做主键，称为：单一主键
create table t_vip(
    id int primary key, //列级约束
    name varchar(255),
    primary key(id) // 表级约束
    );
insert into t_vip(id,name) values(1,'zhangsan');
insert into t_vip(id,name) values(2,'lisi');
-- 错误：不能重复
insert into t_vip(id,name) values(2,'wangwu');
-- ERROR 1062 (23000): Duplicate entry '2' for key 'PRIMARY'
-- 错误：不能为NULL
insert into t_vip(name) values('zhaoliu');
-- ERROR 1364 (HY000): Field 'id' doesn't have a default value
```

#### 8.4.1复合主键

```sql
drop table if exists t_vip;
-- id和name联合起来做主键：复合主键！！！！
create table t_vip(
    id int,
    name varchar(255),
    email varchar(255),
    primary key(id,name)
    );
insert into t_vip(id,name,email) values(1,'zhangsan','zhangsan@123.com');
insert into t_vip(id,name,email) values(1,'lisi','lisi@123.com');
-- 错误：不能重复
insert into t_vip(id,name,email) values(1,'lisi','lisi@123.com');
-- ERROR 1062 (23000): Duplicate entry '1-lisi' for key 'PRIMARY'
```

- 在实际开发中不建议使用复合主键。大部分场景单一主键可以实现标记的作用。
- 一张表，主键约束只能添加1个。（**主键只能有1个**）

```sql
-- 一个表中主键约束能加两个吗？
drop table if exists t_vip;
    create table t_vip(
    id int primary key,
    name varchar(255) primary key
    );
-- ERROR 1068 (42000): Multiple primary key defined
```

**主键分类**

- **自然主键**：主键值是一个自然数，和业务没关系。

- **业务主键**：主键值和业务紧密关联，例如拿银行卡账号做主键值。

#### 8.4.2主键自增

- 在mysql当中，有一种机制，可以帮助我们自动维护一个主键值

```sql
drop table if exists t_vip;
create table t_vip(
    id int primary key auto_increment, //auto_increment表示自增，从1开始，以1递增！
    name varchar(255)
    );
insert into t_vip(name) values('zhangsan');
insert into t_vip(name) values('zhangsan');
insert into t_vip(name) values('zhangsan');
insert into t_vip(name) values('zhangsan');
insert into t_vip(name) values('zhangsan');
insert into t_vip(name) values('zhangsan');
    +----+----------+
    | id | name     |
    +----+----------+
    |  1 | zhangsan |
    |  2 | zhangsan |
    |  3 | zhangsan |
    |  4 | zhangsan |
    |  5 | zhangsan |
```

### 8.5foreign key

- 如果一个实体的某个字段指向另一个实体的主键，就称为外键
- 被指向的实体，称之为主实体（主表），也叫父实体（父表）。
- 负责指向的实体，称之为从实体（从表），也叫子实体（子表）

```sql
create table t_class(
    classno int primary key,
    classname varchar(255)
);
create table t_student(
    no int primary key auto_increment,
    name varchar(255),
    cno int,
    foreign key(cno) references t_class(classno)
    -- t_class是父表，t_student是子表
);
insert into t_class(classno, classname) values(100, '北京市大兴区亦庄镇第二中学高三1班');
insert into t_class(classno, classname) values(101, '北京市大兴区亦庄镇第二中学高三1班');
insert into t_student(name,cno) values('jack', 100);
insert into t_student(name,cno) values('lilei', 100);
insert into t_student(name,cno) values('hanmeimei', 100);
insert into t_student(name,cno) values('zhangsan', 101);
insert into t_student(name,cno) values('lisi', 101);
```

- 外键可以为空，可以理解成 一名学生肯定会关联到一个存在的班级，但来了一个转校生，还没有分班，他现在属于学生子表，但还没有关联到班级主表中的任何一条记录。

​ **删除表**的顺序？ 先删子，再删父。

​ **创建表**的顺序？ 先创建父，再创建子。

​ **删除数据**的顺序？先删子，再删父。

​ **插入数据**的顺序？先插入父，再插入子

- 子表中的外键引用的父表中的某个字段，**被引用字段不一定是主键，但至少具有unique约束**。

## 存储引擎

- 存储引擎是MySQL中特有的一个术语。（Oracle中有有类似概念，但名称不同）
- 存储引擎是一个表存储/组织数据的方式。
- 不同的存储引擎，表存储数据的方式不同。

```sql
show create table t_student;
-- 可以在建表的时候给表指定存储引擎。
CREATE TABLE `t_student` (
    `no` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) DEFAULT NULL,
    `cno` int(11) DEFAULT NULL,
    PRIMARY KEY (`no`),
    KEY `cno` (`cno`),
    CONSTRAINT `t_student_ibfk_1` FOREIGN KEY (`cno`) REFERENCES `t_class` (`classno`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
```

在建表的时候可以在最后小括号的")"的右边使用：

- ENGINE来指定存储引擎。 mysql默认的存储引擎是：**InnoDB**
- CHARSET来指定这张表的字符编码方式。mysql默认的字符编码方式是：**utf8**

### 9.1mysql支持的存储引擎

- `show engines;` 查看mysql支持哪些存储引擎
- mysql支持九大存储引擎，当前5.5.36支持8个。版本不同支持情况不同。

![image-20210917183729616](https://gitee.com/yueliu2345/mysql/raw/master/MYSQL.assets/image-20210917183729616-16318750516641.png)

### 9.2MyISAM存储引擎

- 使用三个文件表示每个表：
  
  - 格式文件 — 存储表结构的定义（mytable.frm）
  - 数据文件 — 存储表行的内容（mytable.MYD）
  - 索引文件 — 存储表上索引（mytable.MYI）：索引是缩小扫描范围，提高查询效率的一种机制。

- MyISAM存储引擎特点：
  
  - 优点：可被转换为压缩、只读表来节省空间。
  - 缺点：MyISAM不支持事务机制，安全性低。

### 9.3InnoDB存储引擎

- 是mysql默认的存储引擎。

- InnoDB支持事务，支持数据库崩溃后自动恢复机制。

- InnoDB存储引擎最主要的特点是：非常安全。

- 它管理的表具有下列主要特征：
  
  - 每个 InnoDB 表在数据库目录中以.frm 格式文件表示
  - InnoDB 表空间 tablespace 被用于存储表的内容（表空间存储数据+索引。）
  - 提供一组用来记录事务性活动的日志文件
  - 用 COMMIT(提交)、SAVEPOINT 及ROLLBACK(回滚)支持事务处理
  - 提供全 ACID 兼容
  - 在 MySQL 服务器崩溃后提供自动恢复
  - 多版本（MVCC）和行级锁定
  - 支持外键及引用的完整性，包括级联删除和更新

- InnoDB最大的特点
  
  - 优点：支持事务：以保证数据的安全。
  
  - 缺点：效率不是很高；不能压缩，不能转换为只读，不能很好的节省存储空间。

### 9.4MEMORY存储引擎

- 使用 MEMORY 存储引擎的表，其数据**存储在内存中**，且行的长度固定，这两个特点使得 MEMORY 存储引擎非常**快**。

- MEMORY 存储引擎管理的表具有下列特征：
  
  - 在数据库目录内，每个表均以.frm 格式的文件表示。
  - 表数据及索引被存储在内存中。（目的就是快，查询快！）
  - 表级锁机制。
  - 不能包含 TEXT 或 BLOB 字段。

- MEMORY 存储引擎以前被称为HEAP 引擎。

- MEMORY引擎特点
  
  - 优点：查询效率是最高的。不需要和硬盘交互。
  
  - 缺点：不安全，关机之后数据消失。因为数据和索引都是在内存当中。

## 10.事务

- 一个事务其实就是一个完整的业务逻辑。是一个最小的工作单元。不可再分。
  
  - 例如转账，从A账户向B账户中转账10000. 将A账户的钱减去10000（update语句） 将B账户的钱加上10000（update语句） 这就是一个完整的业务逻辑。

- **insert**、**delete**、**update**只有以上的三个语句和事务有关系，其它都没有关系。

- 事务：就是**批量的DML语句同时成功，或者同时失败。**

### 10.1InnoDB实现事务

- InnoDB存储引擎：提供一组用来记录事务性活动的日志文件

- 在事务的执行过程中，每一条DML的操作都会记录到“事务性活动的日志文件”中。

- 在事务的执行过程中，**我们可以提交事务，也可以回滚事务。**

- **提交事务 `commit;` 语句**
  
  - 清空事务性活动的日志文件，将数据全部彻底持久化到数据库表中。
  - **提交事务标志着事务的结束**。

- **回滚事务`rollback;`语句**（回滚永远都是只能回滚到上一次的**提交点**）
  
  - 将之前所有的DML操作全部撤销，并且清空事务性活动的日志文件
  - **回滚事务标志着事务的结束**。

- 将mysql的**自动提交机制关闭 `start transaction;`**

##### 回滚事务

```sql
select * from dept_bak;
-- Empty set (0.00 sec)
start transaction;
-- Query OK, 0 rows affected (0.00 sec)
insert into dept_bak values(10,'abc', 'tj');
-- Query OK, 1 row affected (0.00 sec)
insert into dept_bak values(10,'abc', 'tj');
-- Query OK, 1 row affected (0.00 sec)
select * from dept_bak;
-- +--------+-------+------+
-- | DEPTNO | DNAME | LOC |
-- +--------+-------+------+
-- | 10 | abc | tj |
-- | 10 | abc | tj |
-- +--------+-------+------+
-- 2 rows in set (0.00 sec)
rollback;
-- Query OK, 0 rows affected (0.00 sec)
select * from dept_bak;
-- Empty set (0.00 sec)
```

### 10.2事物的四个特性

**A：原子性** 说明事务是最小的工作单元。不可再分。

**C：一致性** 所有事务要求，在同一个事务当中，所有操作必须同时成功，或者同时失败， 以保证数据的一致性。

**I：隔离性** A事务和B事务之间具有一定的隔离。

**D：持久性** 事务最终结束的一个保障。

### 10.3事务的隔离性

#### 10.3.1事务和事务之间四个隔离级别

**读未提交：read uncommitted（最低的隔离级别）《没有提交就读到了》**

- 事务A可以读取到事务B未提交的数据。
- 这种隔离级别存在的问题就是：**脏读现象**！(Dirty Read)，称读到了脏数据。
- 这种隔离级别一般都是理论上的，大多数的数据库隔离级别都是二档起步。

**读已提交：read committed《提交之后才能读到》**

- 事务A只能读取到事务B提交之后的数据。
- 这种隔离级别解决了解决了脏读的现象。
- 这种隔离级别**不可重复读取数据**。
  - 在事务开启之后，第一次读到的数据是3条，当前事务还没有结束，可能第二次再读取的时候，读到的数据是4条，3不等于4称为不可重复读取。
- 这种隔离级别是比较真实的数据，**每一次读到的数据是绝对的真实**。
- oracle数据库默认的隔离级别是：read committed

**可重复读：repeatable read《提交之后也读不到，永远读取的都是刚开启事务时的数据》**

- 事务A开启之后，每次**在事务A中读取到的数据保持一致**。即使事务B将数据已经修改，并且提交了，事务A读取到的数据还是没有发生改变，这就是**可重复读**。

- 可重复读可能会出现幻影读。每一次读取到的数据都是幻象。

- 早晨9点开始开启了事务，只要事务不结束，到晚上9点，读到的数据还是那样！读到的是假象。不够绝对的真实。

- mysql中默认的事务隔离级别。

**序列化/串行化：serializable（最高的隔离级别）**

- 这是最高隔离级别，效率最低。解决了所有的问题。
- 这种隔离级别表示事务排队，不能并发！
- synchronized，线程同步（事务同步）每一次读取到的数据都是最真实的，并且效率是最低的。

#### 10.3.2验证各种隔离级别

- mysql 5 查看隔离级别：`SELECT @@tx_isolation;`
- mysql 8 查看隔离级别：`select @@transaction_isolation;`

```sql
-- 验证：read uncommited
set global transaction isolation level read uncommitted;

-- 验证：read commited
set global transaction isolation level read committed;

-- 验证：repeatable read
set global transaction isolation level repeatable read;

-- 验证：serializable
set global transaction isolation level serializable;
```
