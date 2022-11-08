# 数据说明

## 使用的测试集

+ 总的文件数： 6442893
+ 关键词数： 335362 （精确到小数点后四位）

|测试集文件名|关键词数|文件数|
|:-:|:-:|:-:|
|db_512_80k|512|80000|
|db_1024_80k|1024|80000|
|db_2048_80k|2048|80000|
|db_4096_40k|4096|40000|
|db_4096_60k|4096|60000|
|db_4096_80k|4096|80000|
|db_4096_100k|4096|100000|
|db_4096_120k|4096|120000|
|db_8192_80k|8192|80000|
|db_16384_80k|16384|80000|
|db_65536_1000k|65536|1000000|

## Zuo et al

客户端：

+ 存储关键词与叶子节点的绑定关系

服务器：

+ 存储倒排索引，以节点为关键词
+ 存储的值为 bitmap

测试不同数量的关键词，包括不是 2 的指数的情况。
