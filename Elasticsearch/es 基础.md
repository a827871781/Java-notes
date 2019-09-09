# Elasticsearch

## Elasticsearch的特点

1.  可以作为一个大型分布式集群（数百台服务器）技术，处理PB级数据，服务大公司；也可以运行在单机上，服务小公司
2.  Elasticsearch不是什么新技术，主要是将全文检索、数据分析以及分布式技术，合并在了一起，才形成了独一无二的ES；
3.  对用户而言，是开箱即用的，非常简单，作为中小型的应用，直接3分钟部署一下ES，就可以作为生产环境的系统来使用了，数据量不大，操作不是太复杂
4.  数据库的功能面对很多领域是不够用的（事务，还有各种联机事务型的操作）；特殊的功能，比如全文检索，同义词处理，相关度排名，复杂数据分析，海量数据的近实时处理；Elasticsearch作为传统数据库的一个补充，提供了数据库所不不能提供的很多功能

## Elasticsearch的核心概念

1.  Near Realtime（NRT）：近实时，两个意思，从写入数据到数据可以被搜索到有一个小延迟（大概1秒）；基于es执行搜索和分析可以达到秒级
2.  Cluster：集群，包含多个节点，每个节点属于哪个集群是通过一个配置（集群名称，默认是elasticsearch）来决定的，对于中小型应用来说，刚开始一个集群就一个节点很正常
3.  Node：节点，集群中的一个节点，节点也有一个名称（默认是随机分配的），节点名称很重要（在执行运维管理操作的时候），默认节点会去加入一个名称为“elasticsearch”的集群，如果直接启动一堆节点，那么它们会自动组成一个elasticsearch集群，当然一个节点也可以组成一个elasticsearch集群
4.  Index：索引，包含一堆有相似结构的文档数据
5.  Type：类型，type是index中的一个逻辑数据分类。
6.  Document：文档，es中的最小数据单元，一个document可以是一条客户数据，一条商品分类数据，一条订单数据，通常用JSON数据结构表示。
7.  field ： 数据列。

### Elasticsearch  VS  数据库

| es       | db   |
| -------- | ---- |
| Index    | 库   |
| Type     | 表   |
| Document | 行   |
| field    | 字段 |

### 谨记：

**千万不要将 ES 的一些概念 直接理解为数据库**

**在 ES6.0.0 及更高的版本中，创建的索引只能包含一个映射类型。在 6.0.0 以下的版本中创建的一个索引映射多个类型的索引在 6.0.0 版本中继续发挥作用，但是将在 7.0.0 中完全删除。**

**Index  和 type 的关系是一对一。千万别在一个 index 下创建多个 type ，即使你的版本是 6.0 一下**

## field的类型

粗体常用，其他的了解就行，用的时候 在看，

1.  **字符串 ： text**
-   用于全文索引，该类型的字段将通过分词器进行分词，最终用于构建索引
  
2.  **字符串 - keyword**
-   不分词，只能搜索该字段的完整的值，用于 filtering ，term准确查询，聚合的时候用
  
3.  **数值型**
- long：有符号 64-bit integer：-2^63 ~ 2^63 - 1
    - integer：有符号 32-bit integer，-2^31 ~ 2^31 - 1
    - short：有符号 16-bit integer，-32768 ~ 32767
    - byte： 有符号 8-bit integer，-128 ~ 127
    - double：64-bit IEEE 754 浮点数
    - float：32-bit IEEE 754 浮点数
    - half_float：16-bit IEEE 754 浮点数
    - scaled_float

4.  **布尔 - boolean**
    -   值：false, "false", true, "true"

5.  **日期 - date**
    -   由于 Json 没有 date 类型，所以 es 通过识别字符串是否符合 format 定义的格式来判断是否为 date 类型
    -    format 默认为：`strict_date_optional_time||epoch_millis`[format](https://link.juejin.im/?target=https%3A%2F%2Fwww.elastic.co%2Fguide%2Fen%2Felasticsearch%2Freference%2Fcurrent%2Fmapping-date-format.html)

6.  二进制 - binary
    -   该类型的字段把值当做经过 base64 编码的字符串，默认不存储，且不可搜索

7.  范围类型
    -   范围类型表示值是一个范围，而不是一个具体的值
    -   譬如 age 的类型是 integer_range，那么值可以是 {"gte" : 10, "lte" : 20}；搜索 "term" : {"age": 15} 可以搜索该值；搜索 "range": {"age": {"gte":11, "lte": 15}} 也可以搜索到
    -   range 参数 relation 设置匹配模式
    -   INTERSECTS ：默认的匹配模式，只要搜索值与字段值有交集即可匹配到
    -   WITHIN：字段值需要完全包含在搜索值之内，也就是字段值是搜索值的子集才能匹配
    -   CONTAINS：与 WITHIN 相反，只搜索字段值包含搜索值的文档
    -   integer_range
    -   float_range
    -   long_range
    -   double_range
    -   date_range：64-bit 无符号整数，时间戳（单位：毫秒）
    -   ip_range：IPV4 或 IPV6 格式的字符串

## Elasticsearch query 和 filter 区别

fiter 是精确查询，对待的文档检索的结果是 是 / 否 ；

query 对应文档检索是对文档相关性评分。

### 性能 区别：

filter 返回是和条件匹配的一个简单的列表这是很快可以计算得到的并且也很容易在内存中做缓存；

query 不仅要找到匹配的文档，而且还要计算每个文档的相关性（评分），这就很明显比 filter 花费更多的计算。

## Elasticsearch的 API

### 索引API

#### 创建索引

```js
PUT /${indexName}/
{
    "settings": {
        "index": {
            "number_of_shards": "5",
            "number_of_replicas": "1"
        }
    },
    "mappings": {
        "${typeName}": { 
            "properties": {
                "${fieldNameA}": {
                    "type": "text"
                },
                 "${fieldNameB}": {
                    "type": "long"
                },
                "${fieldNamC}": {
                    "type": "text",
                     "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                }
            }
        }
    }
}

```

#### 索引自创建

如果之前尚未创建索引，则索引操作会自动创建索引，如果尚未创建类型映射，则还会自动为特定类型创建动态类型映射。

讲人话呢，就是没索引，但是可以通过执行新增，创建索引，并新增数据。

不过不建议，默认会在 type 为 text 的字段上 + kayword。

#### keyword 和 text 区别

这两个字段都可以存储字符串使用，但建立索引和搜索的时候是不太一样的

keyword：存储数据时候，不会分词建立索引

text：存储数据时候，会自动分词，并生成索引（这是很智能的，但在有些字段里面是没用的，所以对于有些字段使用text则浪费了空间）。

### GET API

#### _search

全文搜索： 无 keyword 修饰，字段才可以用 全文搜索。

```js
//搜索全部
GET ${indexName}/${typeName}/_search
{
  "query": { "match_all": {} }
}

//根据 Id 获取
GET ${indexName}/${typeName}/${id}
//查询${fieldNamA}包含abc1的商品,同时按照${fieldNamB}降序排序
//全文搜索，会先被拆解，建立倒排索引
//在查询是，会根据不同分词的命中，而展示数据。
GET ${indexName}/${typeName}/_search
{
    "query" : {
        "match" : {
            "${fieldNamA}" : "abc1"
        }
    },
    "sort": [
        { "${fieldNamB}": "desc" }
    ]
}
//分页查询 查询 第二页 第一个
GET ${indexName}/${typeName}/_search
{
  "query": { "match_all": {} },
  "from": 1, 
  "size": 1
}
//指定要查询出来部分字段
GET ${indexName}/${typeName}/_search
{
  "query": { "match_all": {} },
  "_source": ["${fieldNamA}", "${fieldNamC}"]
}

//搜索商品名称包含yagao，而且售价大于25元的商品
//搜索${fieldNamA}包含xx，而且${fieldNamB}大于25
GET ${indexName}/${typeName}/_search
{
    "query" : {
        "bool" : {
            "must" : {
                "match" : {
                    "${fieldNamA}" : "xx" 
                }
            },
            "filter" : {
                "range" : {
                    "${fieldNamB}" : { "gt" : 25 } 
                }
            }
        }
    }
}
//短语搜索
//全文检索相对应，相反，全文检索会将输入的搜索串拆解开来，去倒排索引里面去一一匹配，只要能匹配上任意一个拆解后的单词，就可以作为结果返回
//phrase search，要求输入的搜索串，必须在指定的字段文本中，完全包含一模一样的，才可以算匹配，才能作为结果返回
GET ${indexName}/${typeName}/_search
{
    "query" : {
        "match_phrase" : {
            "${fieldNamB}" : "xx"
        }
    }
}



```

#### aggs

聚合查询字段的 type 要有如下 修饰。

```json
//fielddata:
//将文本field的fielddata属性设置为true
PUT ${indexName}/_mapping/${typeName}
{
  "properties": {
    "${fieldNamB}": {
      "type": "text",
      "fielddata": true
    }
  }
}
//keyword:
//在创建索引时声明keyword 类型
"${fieldNamC}": {
                    "type": "text",
                     "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                }
```

#### fielddata:

当字段被排序，聚合或者通过脚本访问时这种数据结构会被创建。它是通过从磁盘读取每个段的整个反向索引来构建的，然后存存储在java的堆内存中。fileddata默认是不开启的。Fielddata可能会消耗大量的堆空间，尤其是在加载高基数文本字段时。一旦fielddata已加载到堆中，它将在该段的生命周期内保留。此外，加载fielddata是一个昂贵的过程，可能会导致用户遇到延迟命中。

#### keyword:

不会分词，节省空间，提高查询效率。不能分词查询。



```js
//聚合计算${fieldNamB}字段内重复出现的字符数量  对比 SQL group by ${fieldNamB}  count（${fieldNamB} ）
GET ${indexName}/${typeName}/_search
{
  "aggs": {
    "group_by_tags": {
      "terms": { "field": "${fieldNamB}" }
    }
  }
}
// 聚合fieldNamB 字段 对 fieldNamC 求平均值
//sql group by  聚合fieldNamB  avg(fieldNamC)
GET ${indexName}/${typeName}/_search
{
    "size": 0,
    "aggs" : {
        "group_by_tags" : {
            "terms" : { "field" : "${fieldNamB}" },
            "aggs" : {
                "avg_price" : {
                    "avg" : { "field" : "${fieldNamC}"}
                }
            }
        }
    }
}
// 聚合fieldNamB 字段 对 fieldNamC 求平均值,并排序。
//group by fieldNamB avg(fieldNamC) as temp 
//order by temp desc
GET ${indexName}/${typeName}/_search
{
    "size": 0,
    "aggs" : {
        "all_tags" : {
            "terms" : { "field" : "${fieldNamB}", "order": { "${temp}": "desc" } },
            "aggs" : {
                "${temp}" : {
                    "avg" : { "field" : "${fieldNamC}" }
                }
            }
        }
    }
}
//多字段聚合，那么就多字段 一级包一级 aggs计算。 


```

最后，如果一个字段分别需要全文搜索，及聚合查询，那么可以分成两个字段，内容一致，但是 type 不一样。

### 删除一个 type 下所有数据

```http
post http://192.168.1.7:9200/${indexName}/${typeName}/_delete_by_query/
{"query":{"match_all":{}}}
```



