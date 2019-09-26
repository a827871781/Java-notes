# 倒排索引

## 什么是倒排索引

| id   | name | age  | sex  |
| ---- | ---- | ---- | ---- |
| 1    | 张三 | 12   | 男   |
| 2    | 李四 | 28   | 男   |
| 3    | 王五 | 28   | 女   |

类比正排索引:

### 正排为id列创建索引:

| id   | name       |
| ---- | ---------- |
| 1    | 张三-12-男 |
| 2    | 李四-28-男 |
| 3    | 王五-28-女 |

### 倒排为id列创建索引:

#### name

| Term |	Posting List|
| ----| ----|
|张三	|1|
|李四|	2|
|王五	|3 |

#### age

| Term | Posting List |
| ---- | ------------ |
| 28   | [2,3]        |
| 12   | 1            |

#### sex

| Term | Posting List |
| ---- | ------------ |
| 28   | [1,2]        |
| 女   | 3            |

### Posting List

Elasticsearch 分别为每个 field 都建立了一个倒排索引。

女, 28, 张三, 李四 这些叫 term.

Posting list 就是一个 int数组，存储了所有符合某个term的文档id。
通过 posting list 这种索引方式似乎可以很快进行查找.

### Term Dictionary

Elasticsearch 为了能快速找到某个 term，将所有的 term排序，二分法查找term，logN的查找效率，就像通过字典树查找一样，这就是 Term Dictionary。本次创建的Term DIctionary 顺序就是 age / name / sex .



### Term Index

B-Tree 通过减少磁盘寻道次数来提高查询性能，Elasticsearch 也是采用同样的思路，直接通过内存查找 term，不读磁盘，但是如果 term 太多，term dictionary 也会很大，放内存不现实，于是有了 Term Index，就像字典里的索引页一样，A 开头的有哪些 term，分别在哪页，可以理解 term index 是一颗树.

这棵树不会包含所有的 term，它包含的是 term的一些前缀。通过 term index 可以快速地定位到 term dictionary的某个offset，然后从这个位置再往后顺序查找。

![af62c5d0-dde8-11e9-8290-acde48001122](https://i.loli.net/2019/09/23/ENc7CBayHRQnTIW.png )



term index 不需要存下所有的 term，而仅仅是他们的一些前缀与Term Dictionary的block之间的映射关系。再结合 FST 的压缩技术，可以使 term index 缓存到内存中。从 term index 查到对应的 term dictionary 的 block 位置之后，再去磁盘上找 term，大大减少了磁盘随机读的次数。

**正排索引：从id角度看其中的属性值，表示每个文档（用文档 ID 标识）都含有哪些属性值。**

**倒排索引：从属性值看id，标识每个属性值分别在那些文档中出现 (文档 ID)。**

**正排索引:就是方便通过id查询的索引.**

**倒排索引:通过索引其他列内容查询出id的索引.**



## 基于以上结果可以得出如下简单结论:

### 1.倒排索引,内存占用大

### 2.倒排索引,适用于模糊查询,列表查询.全文搜索





