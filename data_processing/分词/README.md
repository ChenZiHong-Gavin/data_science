# 打造自己的分词器

## 为什么要分词

在数据科学的领域，对于一般的统计数据，如数字，输入计算机，经过清洗便可以用来建模预测。 而我们常见的文本和图片也是一种数据，只是和便于操作的表格数据不一样罢了，所以问题来了，如何把文本和图片这样特殊的数据， 输入到计算机，用来做分类识别呢。这便是分词的目的。

对于中文文本就用到了自然语言处理NLP（Natural Language Processing），将一行行文字，生成计算机模型可以 处理的数字和向量表达，最终达到可以被计算机识别，模型使用，预测分类的作用。

分词是中文自然语言处理基础且重要的任务。词是表意的完整单位。“张三”这个词中，“张”其实既可以是姓也可以表“张开”之意，而“三”则常被表示为数字。但“张三”作为一个词出现在一起时，大家明确知道这表示的是个人名，故而句子经过分词后可降低理解的难度。

分词也是文本检索、知识图谱等自然语言处理应用的重要基础。这些下游任务的效果很大程度受限于分词的准确率。在问答对话、信息抽取、机器翻译等任务也常用采用分词后的结果作为模型输入。在深度学习模型中，**分词除了能降低学习难度外，还可以缩短输入序列长度，从而降低模型运算量**。

## 为什么要拥有属于自己的分词器

对于分词标准问题，总是众口难调的，因为分词标准上存在人的主观性，而且其实**对于不同的应用，所需要的分词粒度也是不同的**。比如检索相关的应用往往偏向于更细粒度的分词，甚至同时使用多种粒度的分词构建索引，如果我们仅仅采用粗粒度的分词，就会难以匹配到预期的结果。而在医疗、音乐、法律等不同应用领域，所采用的分词标准往往也是有所差异的。这个时候我们就需要打造一个属于自己的**个性化分词**工具。

## 分词工具

mecab 是基于CRF 的一个日文分词系统，代码使用 c++ 实现， 基本上内嵌了 CRF++ 的代码， 同时提供了多种脚本语言调用的接口(python, perl， ruby 等).整个系统的架构采用通用泛化的设计， 用户可以通过配置文件定制CRF训练中需要使用的特征模板。 如果你有中文的分词语料作为训练语料，可以在该架构下按照其配置文件的规范定制一个中文的分词系统。

## 个性化分词的实现

1. 安装MeCab和mecab-python插件

2. 准备Seed词典

   MeCab 的词典是 CSV 格式的。Seed 词典和用于发布的词典的格式基本上是相同的。

   形如：

   １１２３项,0,0,0,0,0,0
   义演,0,0,0,0,0,0
   佳酿,0,0,0,0,0,0
   沿街,0,0,0,0,0,0
   老理,0,0,0,0,0,0
   三四十岁,0,0,0,0,0,0
   解波,0,0,0,0,0,0
   统建,0,0,0,0,0,0
   蓓蕾,0,0,0,0,0,0
   李佑生,0,0,0,0,0,0

   使用script中的make_mecab_seed_data.py制作seed词典

3. 准备配置文件

   分别是：

   1) [dicrc](https://github.com/panyang/yuzhen_nlp_edu_tools/blob/master/CLPT/WordSegmentation/MeCab/seed/dicrc): 该文件中设定词典的各种动作的

   2) [char.def](https://github.com/panyang/yuzhen_nlp_edu_tools/blob/master/CLPT/WordSegmentation/MeCab/seed/char.def): 定义未登陆词处理的文件. 通常日语的词法分析是基于字符的种类处理未登陆词, Mecab 中哪个文字属于哪个字符种类, 用户可以进行细致的指定; 对于每个字符类别， 需要采用哪种未登陆词的识别处理,也可以进行详细的定义。

   3) [unk.def](https://github.com/panyang/yuzhen_nlp_edu_tools/blob/master/CLPT/WordSegmentation/MeCab/seed/unk.def): 用于未登陆词的词典。

   4) [rewrite.def](https://github.com/panyang/yuzhen_nlp_edu_tools/blob/master/CLPT/WordSegmentation/MeCab/seed/rewrite.def): 定义从特征列到内部状态特征列的转换映射。

   5) [feature.def](https://github.com/panyang/yuzhen_nlp_edu_tools/blob/master/CLPT/WordSegmentation/MeCab/seed/feature.def): 该文件中定义了从内部状态的素生列中抽取CRF的素生列的模板

4. 准备训练语料

   我们的中文分词训练语料来源于icwb2-data/training/msr_training.utf8 ，和词典格式一样，我们提供一份格式非常简单的用于MeCab训练的分词语料，如下所示：

   “ 0,0,0,0,0,0
   人们 0,0,0,0,0,0
   常 0,0,0,0,0,0
   说 0,0,0,0,0,0
   生活 0,0,0,0,0,0
   是 0,0,0,0,0,0
   一 0,0,0,0,0,0
   部 0,0,0,0,0,0
   教科书 0,0,0,0,0,0
   ， 0,0,0,0,0,0

   同样提供一个可用于语料格式转换的脚本：[make_mecab_train_data.py](https://github.com/panyang/yuzhen_nlp_edu_tools/blob/master/CLPT/WordSegmentation/MeCab/script/make_mecab_train_data.py)

5. 生成训练用的二进制词典

6. CRF模型参数训练

7. 生成用于发布的词典

8. 生成用于解析器的词典

9. 在命令行调用命令`mecab -d ./final/`即可得到分词结果

10. 使用测试脚本评估MeCab中文分词的准确率
