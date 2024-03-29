# LeC.0853.Car-Fleet

## 题目

`N` cars are going to the same destination along a one lane road. The destination is `target` miles away.

Each car `i` has a constant speed `speed[i]` (in miles per hour), and initial position `position[i]` miles towards the target along the road.

A car can never pass another car ahead of it, but it can catch up to it, and drive bumper to bumper at the same speed.

The distance between these two cars is ignored - they are assumed to have the same position.

A *car fleet* is some non-empty set of cars driving at the same position and same speed. Note that a single car is also a car fleet.

If a car catches up to a car fleet right at the destination point, it will still be considered as one car fleet.

How many car fleets will arrive at the destination?

**Example 1:**

    Input: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
    Output: 3
    Explanation:
    The cars starting at 10 and 8 become a fleet, meeting each other at 12.
    The car starting at 0 doesn't catch up to any other car, so it is a fleet by itself.
    The cars starting at 5 and 3 become a fleet, meeting each other at 6.
    Note that no other cars meet these fleets before the destination, so the answer is 3.

**Note:**

1. `0 <= N <= 10 ^ 4`
2. `0 < target <= 10 ^ 6`
3. `0 < speed[i] <= 10 ^ 6`
4. `0 <= position[i] < target`
5. All initial positions are different.

## 题目大意

N  辆车沿着一条车道驶向位于 target 英里之外的共同目的地。每辆车 i 以恒定的速度 speed[i] （英里/小时），从初始位置 position[i] （英里） 沿车道驶向目的地。

一辆车永远不会超过前面的另一辆车，但它可以追上去，并与前车以相同的速度紧接着行驶。此时，我们会忽略这两辆车之间的距离，也就是说，它们被假定处于相同的位置。车队 是一些由行驶在相同位置、具有相同速度的车组成的非空集合。注意，一辆车也可以是一个车队。即便一辆车在目的地才赶上了一个车队，它们仍然会被视作是同一个车队。

 问最后会有多少车队到达目的地?

## 解题思路

- 根据每辆车距离终点和速度，计算每辆车到达终点的时间，并按照距离从大到小排序(position 越大代表距离终点越近)
- 从头往后扫描排序以后的数组，时间一旦大于前一个 car 的时间，就会生成一个新的 car fleet，最终计数加一即可。

**示例 1：**

```
输入：target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
输出：3
解释：
从 10 和 8 开始的车会组成一个车队，它们在 12 处相遇。
从 0 处开始的车无法追上其它车，所以它自己就是一个车队。
从 5 和 3 开始的车会组成一个车队，它们在 6 处相遇。
请注意，在到达目的地之前没有其它车会遇到这些车队，所以答案是 3。
```

**示例 2:**

```
输入: target = 10, position = [3], speed = [3]
输出: 1
解释: 只有一辆车，因此只有一个车队。
```

**示例 3:**

```
输入: target = 100, position = [0,2,4], speed = [4,2,1]
输出: 1
解释:
以0(速度4)和2(速度2)出发的车辆组成车队，在4点相遇。舰队以2的速度前进。
然后，车队(速度2)和以4(速度1)出发的汽车组成一个车队，在6点相遇。舰队以1的速度前进，直到到达目标。
```

**提示：**

- `n == position.length == speed.length`
- `1 <= n <= 105`
- `0 < target <= 106`
- `0 <= position[i] < target`
- `position` 中每个值都 **不同**
- `0 < speed[i] <= 106`

**题解**

```go

```
