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

-- 1.基础条件查询
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

-- 2.排序
-- (1) asc默认升序**`select 字段 from 表名 order by 字段;`(ascend)
-- (2) desc指定降序**`select 字段 from 表名 order by 字段 desc;`(descend)
-- (3) 多个条件时，只有前面的条件都相等，才会启用后面的排序条件
select `name` from t_student order by `age`;
select `name` from t_student order by `age` desc;
select `name` from t_student order by `age` desc, `name` asc; -- 前等后排

-- 3.分页
-- (1) limit 分页查询             limit [startIndex], length;
-- (2) 每页pageSize条，第pageNo页：limit (pageNo - 1) * pageSize , pageSize
select name,sex from t_student order by id desc limit 5; -- 取id降序前5
select name,sex from t_student order by id desc limit 3,2; -- 取id 4-5

-- 4.Union
-- (1) union     将两条 select 语句结果合并显示，（select语句字段数量必须相同）
-- (2) union all 将所有的结果全部显示出来，即便重复（字段顺序以首个select语句为准）
```

```sql
-- #############################################################
-- 函数
-- #############################################################

-- 单行处理函数(一个输入对应一个输出)
-- (1) lower/upper 转换小写/大写
select lower(name) as name from t_student;
-- (2)substr( 被截取的字符串, 起始下标, 截取的长度); 取子串 
select substr(name, 1, 1) as name from emp;
select name from t_student where name like 'A%'; -- 名字首字母为A的学生
select name from t_student where substr(ename,1,1) = 'A'; -- 同上
-- (3) concat 字符串拼接
select concat(name,'--',age) as 'name&age' from t_student;
-- (4) length 返回字符串长度
select length(name) namelength from t_student;
-- (5) trim 去空格
select trim(name),trim(age) from t_student where id='3';
-- (6) str_to_date 将字符串转换成日期
select STR_TO_DATE('2017-01-06 10:20:30','%H:%i:%s') AS result1;
select STR_TO_DATE('2017-01-06 10:20:30','%Y-%m-%d') AS result2;
-- (7) date_format 以不同格式显示时间数据
date_format(NOW(),'%b %d %Y %h:%i %p')
date_format(NOW(),'%m-%d-%Y')
-- | %Y  | 年，4 位 |
-- | %y  | 年，2 位 |
-- | %M  | 月名  |
-- | %m  | 月，数值(00-12) |
-- | %b  | 缩写月名 |
-- | %D  | 带有英文前缀的月中的天 |
-- | %d  | 月的天，数值(00-31) |
-- | %e  | 月的天，数值(0-31) |
-- | %H  | 小时 (00-23) |
-- | %h  | 小时 (01-12) |
-- | %I  | 小时 (01-12) |
-- | %k  | 小时 (0-23) |
-- | %l  | 小时 (1-12) |
-- | %i  | 分钟，数值(00-59) |
-- | %S  | 秒(00-59) |
-- | %s  | 秒(00-59) |
-- | %p  | AM 或 PM |
-- | %r  | 时间，12-小时（hh:mm:ss AM 或 PM） |
-- | %T  | 时间, 24-小时 (hh:mm:ss) |
-- (8) format(N,D,locale); 设置千分位(N 被格式化数字, D 小数位数, locale 分隔符)
select format(14500.2018, 2); -- 保留两位小数
select concat('￥',format(100*3, 0)); -- 不保留小数
-- (9) round 保留小数
select round(1236.567, 1) as result from t_student; -- 保留1个小数
select round(1236.567, 2) as result from t_student; -- 保留2个小数
select round(1236.567, -1) as result from t_student; -- 保留到十位。
-- (10) rand 生成随机数
select round(rand()*100,0) from t_student; -- 100以内的随机数
-- (11) ifnull(表达式1,表达式2); 可以将 null 转换成一个具体值
-- 表达式1不为NULL，则函数返回表达式1; 否则返回表达式2的结果。
select name,IFNULL(email,'guest@163.com') email from t_student;
-- (12) datediff(startdate,date2) 返回startdate和enddate间的间隔的天数
SELECT datediff('2008-11-30','2008-11-29') AS DiffDate
SELECT datediff('2008-11-29','2008-11-30') AS DiffDate

-- 分组函数(输入多行，单行输出)
-- (1) count 计数
select count(name) from t_student;
-- (2) sum 求和
select sum(age) from t_student;
-- (3) avg 平均值
select avg(age) from t_student;
-- (4) max 最大值
select max(age) from t_student;
-- (5) min 最小值
select min(age) from t_student;
-- (1) 先分组，默认一张表为一组
-- (2) 分组函数自动忽略NULL
-- (3) count(字段)：该字段不为NULL的元素数;count(*)：统计表中总行数。
-- (4) 分组函数不能直接用于where子句中
```

```sql
-- #############################################################
-- 分组查询
-- #############################################################

-- (1) 分组查询：group by 存在时，select后面只能跟：参加分组的字段、分组函数
select job,sum(sal) from emp group by job; -- 各部门最高薪资
-- (2) 联合分组：多个字段作为1个字段
select dep,job,max(sal) from emp group by dep,job; -- 各部门，不同岗最高薪资
-- (3) having ①必须和group by联合使用;②对分组后的数据进行筛选;③优先用where
select dep,avg(sal) from emp group by dep having avg(sal) > 2500;
-- (4) 关键字书写顺序
-- select --> from --> where --> group by --> having --> order by
-- (5) 关键字执行顺序
-- 1. 从某张表中查询数据。               （from）
-- 2. 先经过where条件筛选出有价值的数据。  （where）
-- 3. 对这些有价值的数据进行分组。        （group by）
-- 4. 分组之后可以使用having继续筛选。    （having）
-- 5. select查询出来。                 （select）
-- 6. 最后排序输出。                    （order by）
```

```sql
-- #############################################################
-- 连表查询
-- #############################################################

-- (0) 笛卡尔积：无条件限制，查询条数为两张表条数之积
select ename,dname from emp, dept;
-- (1) 内连接-等值连接
select e.ename,d.dname from emp e inner join dept d on e.deptno = d.deptno;
-- (2) 内连接-非等值连接
select e.ename, e.sal, s.grade -- 每个员工的薪资等级，要求显示员工名、薪资、薪资等级
from emp e join salgrade s 
on e.sal between s.losal and s.hisal; 
-- (3) 内连接-自连接 
select a.ename as '员工名', b.ename as '领导名'
from emp a -- 查询员工的上级领导，要求显示员工名和对应的领导名
join emp b
on a.mgr = b.empno;
-- (4) 外连接
-- | inner join | 如果表中至少有一个匹配，就返回值      |
-- | left join  | 会从左表中返回所有的值，即使右表中没有匹配 |
-- | right join | 会从右表中返回所有的值，即使左表中没有匹配 |
select e.ename,d.dname -- outer可省略。
from emp e 
right outer join dept d
on e.deptno = d.deptno;

select e.ename,d.dname 
from dept d 
left outer join emp e
on e.deptno = d.deptno;
-- (5) 多表连接
-- 语法：
    select     ...
    from       a
    join       b
    on         a和b的连接条件
    join       c
    on         a和c的连接条件
    right join d
    on         a和d的连接条件
-- 找出每个员工的部门名称以及工资等级，要求显示员工名、部门名、薪资、薪资等级？
select e.ename,e.sal,d.dname,s.grade
from emp e
join dept d
on e.deptno = d.deptno
join salgrade s 
on e.sal between s.losal and s.hisal;
-- 找出每个员工的部门名称以及工资等级，还有上级领导，要求显示员工名、领导名、部门名、薪资、薪资等级？
select e.ename,e.sal,d.dname,s.grade,l.ename
from emp e
join dept d
on e.deptno = d.deptno
join salgrade s
on e.sal between s.losal and s.hisal
left join emp l
on e.mgr = l.empno;
```

```sql
-- #############################################################
-- 子查询
-- #############################################################

-- 子查询可以出现在 select、from、where 后面
select ename,sal from emp where sal > (select min(sal) from emp);
-- 找出每个岗位的平均工资的薪资等级。
select t.*, s.grade -- 将子查询的查询结果当做一张临时表
from (select job,avg(sal) as avgsal from emp group by job) t 
join salgrade s
on t.avgsal between s.losal and s.hisal;
```

```sql
-- #############################################################
-- 约束
-- #############################################################

-- (0) 约束类型
-- 非空约束：not null
-- 唯一性约束: unique
-- 主键约束: primary key
-- 外键约束：foreign key
-- 检查约束：check（mysql不支持，oracle支持）
```
