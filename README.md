# danmu_wc
将B站弹幕生成词云, (只是简单的api使用)

### Example
[爱酱的生化危机合集](https://space.bilibili.com/1473830/#/channel/detail?cid=28784)  

![花Q]()  

> 也想过写一个通过channel频道添加合集里相关aid的方法, 但是这涉及到B站账号的登陆操作, 实现起来太麻烦, 比较简单的方法可以使用example文件夹里的例子, 将合集页面的html保存到本地去解析

### Basic Usage
```python
from danmu import Danmu
d = Danmu(aid='10000000')  # 可以输入初始的aid号
d.add_aid('20000000')  # 也可以通过add_aid方法添加
d.generate_wc()  # 然后直接生成
```

`generate_wc()`可调参数:  
* img_file: 背景图文件名
* colored: 是否使用背景图底色(只有在背景图设置了的情况下才有效)
* userdict: 自定义词汇字典(txt文本格式, 一个词占一行, 为jieba分词使用)
* stopwords: 停用词字典(同样txt文本格式, 一个词一行, ban掉部分不想看到的词)
* output: 生成图片名(默认为result.jpg)
* 其余参数参考wordcloud的`generate()`方法

### Requirements
* python3.5+
* wordcloud
* jieba
* requests
* lxml
* numpy
* PIL
> numpy与PIL是为了生成图像词云, 也有不需要这两个库的方法, 倒是懒得搞了...

