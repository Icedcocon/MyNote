### Flow chart

- (1) A node (with text)

```mermaid
flowchart LR
  test[this is text in node]
```

- (2) Graph

```mermaid
flowchart LR
  node1 --> node2
```

```mermaid
flowchart TD
    Start --> Stop
```

- (3) A node (with round edges)

```mermaid
flowchart LR
  id(This is the text in the box)
```

- (4) A stadium-shaped node

```mermaid
flowchart LR
id([This is the text in the box])
```

- (5) A node in a subroutine shape

```mermaid
flowchart LR
    id[[This is the text in the box]]
```

- (6) A node in a cylindrical shape

```mermaid
flowchart LR
    id[(Database)]
```

## 流程图方向

- TB - top to bottom

- TD - top-down/ same as top to bottom

- BT - bottom to top

- RL - right to left

- LR - left to right

```mermaid
<style>

</style>
flowchart TD
  subgraph Pod
    direction LR
    id1[Pause]
    id2[user container1]
    id3[user container2]
    id4[user containerN]
  end
```
