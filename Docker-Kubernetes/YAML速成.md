```yaml
################
# YAML简介及注释
################
# (1) 是 JSON 的严格超集
# (2) 语法上增加了换行符和缩进
# (3) YAML 不允许使用文字制表符（tab）表示缩进
# (4) 文件名以.yaml结尾
# (5) 大小写敏感

# YAML 中的注释看起来像这样。

################
# 基本数据类型
################
# YAML擅长处理映射表(哈希表 / 字典)、序列(数组 / 列表)和标量(字符串 / 数字)
"标量类型":
  - integer: 25
  - float: 25.0
  - string: "25"
  - boolean: Yes
"容器类型":
  - "List"
  - "Map"

################
# 序列
################
# (1) 列表或者数组。每个item一行，以-开头。
- Cat
- Dog
- Goldfish
# (2) 同一层级的item是一个序列，可以用缩进来表示多层的序列。
-
  - Cat
  - Dog
  - Goldfish
-
  - Python
  - Lion
  - Tiger
# (3) 可以是多层的：
-
 -
  - Cat
  - Dog
  - Goldfish
# (4) 同上
--- Cat
  - Dog
  - Goldfish

################
# 映射表
################
# (1) 键值对
animal: pets
# (2) 如果值是一个序列
pets:
  - Cat
  - Dog
  - Goldfish

################
# 标量类型       
################

# 根对象是一个map，相当于其它语言中的dictionary、hash或者object。
key: value
another_key: Another value goes here.
a_number_value: 100
scientific_notation: 1e+12

# 数字 1 会被解释为数值，想要表示布尔值，使用 true。
boolean: true
null_value: null
key with spaces: value

# 字符串不需要使用引号，不过可以使用。
however: '包裹在单引号中的字符串'
'Keys can be quoted too.': "Useful if you want to put a ':' in your key."
single quotes: 'have ''one'' escape pattern'
double quotes: "have many: \", \0, \t, \u263A, \x0d\x0a == \r\n, and more."

# UTF-8/16/32字符需要指明编码（通过\u）。
Superscript two: \u00B2

# 多行字符串既可以写成一个'字面量块'(使用 '|')，
# 也可以写成一个'折叠块'(使用 '>')。
literal_block: |
    This entire block of text will be the value of the 'literal_block' key,
    with line breaks being preserved.

    The literal continues until de-dented, and the leading indentation is
    stripped.

        Any lines that are 'more-indented' keep the rest of their indentation -
        these lines will be indented by 4 spaces.
folded_style: >
    This entire block of text will be the value of 'folded_style', but this
    time, all newlines will be replaced with a single space.

    Blank lines, like above, are converted to a newline character.

        'More-indented' lines keep their newlines, too -
        this text will appear over two lines.

####################
# 集合类型         #
####################

# 嵌套是通过缩进完成的。推荐使用 2 个空格的缩进（但非必须）。
a_nested_map:
  key: value
  another_key: Another Value
  another_nested_map:
    hello: hello

# 映射的键不必是字符串。
0.25: a float key

# 键也可以是复合（complex）的，比如多行对象
# 我们用 '?' 后跟一个空格来表示一个复合键的开始。
? |
  This is a key
  that has multiple lines
: and this is its value

# YAML 也允许使用复杂键语法表示序列间的映射关系。
# 但有些解析器可能会不支持。
# 一个例子：
? - Manchester United
  - Real Madrid
: [ 2001-01-01, 2002-02-02 ]

# 序列 (sequences，等价于列表 list 或数组 array ) 看起来像这样：
# 注意 '-' 也算缩进：
a_sequence:
  - Item 1
  - Item 2
  - 0.5 # 序列可以包含不同类型。
  - Item 4
  - key: value
    another_key: another_value
  -
    - This is a sequence
    - inside another sequence
  - - - Nested sequence indicators
      - can be collapsed

# 因为 YAML 是 JSON 的超集，你也可以写 JSON 风格的映射和序列：
json_map: {"key": "value"}
json_seq: [3, 2, 1, "takeoff"]
and quotes are optional: {key: [3, 2, 1, takeoff]}

#######################
# 其余的 YAML 特性    #
#######################

# YAML 还有一个方便的特性叫“锚”（anchors）。你可以使用它在文档中轻松地完成文本复用。
# 如下两个键会有相同的值：
anchored_content: &anchor_name This string will appear as the value of two keys.
other_anchor: *anchor_name

# 锚也可被用来复制/继承属性
base: &base
  name: Everyone has same name

# '<<'称为语言无关的合并键类型（Merge Key Language-Independent Type）.
# 它表明一个或多个指定映射中的所有键值会插入到当前的映射中。

foo: &foo
  <<: *base
  age: 10

bar: &bar
  <<: *base
  age: 20

# foo 和 bar 将都含有 name: Everyone has same name

# YAML 还有标签（tags），你可以用它显式地声明类型。
explicit_string: !!str 0.5
# 一些解析器实现了特定语言的标签，就像这个针对Python的复数类型的标签。
python_complex_number: !!python/complex 1+2j

# 我们也可以在 YAML 的复合键中使用特定语言的标签：
? !!python/tuple [5, 7]
: Fifty Seven
# 将会是 Python 中的 {(5, 7): 'Fifty Seven'}

####################
# 其余的 YAML 类型 #
####################

# 除了字符串和数字，YAML 还支持其它标量。
# ISO 格式的日期和时间字面量也可以被解析。
datetime: 2001-12-15T02:59:43.1Z
datetime_with_spaces: 2001-12-14 21:59:43.10 -5
date: 2002-12-14

# 这个 !!binary 标签表明这个字符串实际上
# 是一个用 base64 编码表示的二进制 blob。
gif_file: !!binary |
  R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J+fn5
  OTk6enp56enmlpaWNjY6Ojo4SEhP/++f/++f/++f/++f/++f/++f/++f/++f/+
  +f/++f/++f/++f/++f/++SH+Dk1hZGUgd2l0aCBHSU1QACwAAAAADAAMAAAFLC
  AgjoEwnuNAFOhpEMTRiggcz4BNJHrv/zCFcLiwMWYNG84BwwEeECcgggoBADs=

# YAML 还有一个集合（set）类型，它看起来像这样：
set:
  ? item1
  ? item2
  ? item3
or: {item1, item2, item3}

# 集合只是值均为 null 的映射；上面的集合等价于：
set2:
  item1: null
  item2: null
  item3: null

...  # 文档结束
```
