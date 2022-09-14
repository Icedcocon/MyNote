### 175.组合两个表

- 联表查询

```sql
SELECT `p`.`FirstName`,`p`.`LastName`,`a`.`City`,`a`.`State` 
FROM `Person` AS `p`
LEFT JOIN `Address` AS `a`
ON `p`.`PersonId` = `a`.`PersonId`;
```

### 595.大的国家

- 条件查询

```sql
SELECT `name`,`population`,`area`
FROM WORLD
WHERE `area` >= 3000000
OR `population` >= 25000000;
```

### 181.超过经理收入的员工

- 联表查询、自连接

```sql
SELECT `e`.`name` AS 'Employee'
FROM `Employee` AS `e`
INNER JOIN `Employee` AS `m`
ON `e`.`managerId` = `m`.`id`
AND `e`.`salary` > `m`.`salary`;
```

- 条件查询、自连接

```sql
SELECT `e`.`name` AS 'Employee'
FROM `Employee` as `e`, `Employee` as `m`
WHERE `e`.`managerId` = `m`.`id`
AND `e`.`salary` > `m`.`salary`;
```

### 196.删除重复的电子邮箱

- 删除、自连接

```sql
DELETE `p1`
FROM `Person` AS `p1`, `Person` AS `p2`
WHERE `p1`.`email` = `p2`.`email`
AND `p1`.`id` > `p2`.`id`;
```

### 511.游戏玩法分析 I

- 分组查询、分组函数

```sql
SELECT `player_id`,MIN(`event_date`) AS `first_login`
FROM `Activity`
GROUP BY `player_id`;
```

### 197.上升的温度

- DATEDIFF()

```sql
SELECT `w1`.`id`
FROM `Weather` `w1`
INNER JOIN `Weather` `w2`
ON DATEDIFF(`w1`.`recordDate`,`w2`.`recordDate`) = 1
AND `w1`.`temperature` > `w2`.`temperature`;
```

### 596.超过5名学生的课

- 子查询、COUNT

```sql
SELECT `class`
FROM
(
    SELECT `class`, COUNT(DISTINCT `student`) AS `num`
    FROM `Courses`
    GROUP BY `class`
) AS `temp_table`
WHERE `num` >= 5;
```

- GROUP BY、 HAVING

```sql
SELECT `class`
FROM `Courses`
GROUP BY `class`
HAVING COUNT(DISTINCT student) >= 5;
```
