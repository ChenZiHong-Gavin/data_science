import json


def text():
    # 一行一条评论
    f1 = open('good.txt', 'r', encoding='utf-8')
    f2 = open('bad.txt', 'r', encoding='utf-8')
    line1 = f1.readline()
    line2 = f2.readline()
    s = ''
    while line1:
        s += line1
        line1 = f1.readline()
    while line2:
        s += line2
        line2 = f2.readline()
    f1.close()
    f2.close()
    return s


# 其余分类方法可以参见oneWord，twoWords，mixedWords


# 使用分词后的列表作为特征选取的依据
from pyhanlp import *


def readfile(filename):
    f = open(filename, 'r', encoding='utf-8')
    line = f.readline()
    re = []
    while line:
        # 关闭词性
        HanLP.Config.ShowTermNature = False
        # 停用词过滤
        CoreStopWordDictionary = JClass('com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary')
        term_list = HanLP.segment(line)
        CoreStopWordDictionary.apply(term_list)
        re.append(term_list)
        line = f.readline()
    return re


from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.metrics import BigramAssocMeasures


# 进行卡方统计


def getFeature(number):
    posWords = []
    negWords = []
    for items in readfile('good.txt'):
        for item in items:
            posWords.append(str(item))
    for items in readfile('bad.txt'):
        for item in items:
            negWords.append(str(item))
    word_fd = FreqDist()  # 可统计所有词的词频
    con_word_fd = ConditionalFreqDist()  # 可统计积极文本中的词频和消极文本中的词频
    for word in posWords:
        word_fd[str(word)] += 1
        con_word_fd['pos'][str(word)] += 1

    for word in negWords:
        word_fd[str(word)] += 1
        con_word_fd['neg'][str(word)] += 1
    pos_word_count = con_word_fd['pos'].N()  # 积极词的数量
    neg_word_count = con_word_fd['neg'].N()  # 消极词的数量
    # 一个词的信息量等于积极卡方统计量加上消极卡方统计量
    total_word_count = pos_word_count + neg_word_count
    word_scores = {}
    for word, freq in word_fd.items():
        pos_score = BigramAssocMeasures.chi_sq(con_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(con_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score
        best_vals = sorted(word_scores.items(), key=lambda item: item[1],
                           reverse=True)[:number]
    best_words = set([w for w, s in best_vals])
    return dict([(str(word), True) for word in best_words])


# 这里改变特征值的维度
feature = getFeature(200)

# 构建训练需要的数据格式：
def build_features():
    posFeatures = []
    for items in readfile('good.txt'):
        a = {}
        for item in items:
            if str(item) in feature.keys():
                a[str(item)] = 'True'
        if a != {}:
            posWords = [a, 'pos']  # 为积极文本赋予"pos"
            posFeatures.append(posWords)
    negFeatures = []
    for items in readfile('bad.txt'):
        a = {}
        for item in items:
            if str(item) in feature.keys():
                a[str(item)] = 'True'
        if a != {}:
            negWords = [a, 'neg']  # 为消极文本赋予"neg"
            negFeatures.append(negWords)
    return posFeatures, negFeatures


posFeatures, negFeatures = build_features()
from random import shuffle

shuffle(posFeatures)  # 把文本的排列随机化
shuffle(negFeatures)

train = posFeatures[int(len(posFeatures) * 0.2):] + negFeatures[int(len(negFeatures) * 0.2):]
# 二八原则
test = posFeatures[:int(len(posFeatures) * 0.2)] + negFeatures[:int(len(negFeatures) * 0.2)]
data, tag = zip(*test)  # 分离测试集合的数据和标签，便于测试

from nltk.classify.scikitlearn import SklearnClassifier


def score(classifier):
    classifier = SklearnClassifier(classifier)
    classifier.train(train)
    pred = classifier.classify_many(data)
    n = 0
    s = len(pred)
    for i in range(0, s):
        if (pred[i] == tag[i]):
            n = n + 1
    return n / s


# 通过实验，比较预测准确度score进而得出最佳特征提取方式、最佳特征维度、最佳分类算法
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

print('LogisticRegression`s accuracy is  %f' % score(LogisticRegression()))
print('SVC`s accuracy is  %f' % score(SVC()))
print('LinerSVC`s accuracy is  %f' % score(LinearSVC()))
print('NuSVC`s accuracy is  %f' % score(NuSVC()))
print('MultinomialNB`s accuracy is  %f' % score(MultinomialNB()))
print('BernoulliNB`s accuracy is  %f' % score(BernoulliNB()))


# 处理输入的评论文本，使其成为可预测格式
def build_page(page):
    feature4 = feature
    temp = {}

    # 分词形式处理待测文本

    # 关闭词性
    HanLP.Config.ShowTermNature = False
    # 停用词过滤
    CoreStopWordDictionary = JClass('com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary')
    term_list = HanLP.segment(page)
    CoreStopWordDictionary.apply(term_list)
    for items in term_list:
        if str(items) in feature4:
            temp[str(items)] = 'True'
    return temp


# 将实验比较得出的最佳分类算法（classifier_ag）构造的分类器保存
def classfier_model(classifier_ag):
    classifier = SklearnClassifier(classifier_ag)
    classifier.train(train)
    return classifier


# 假设逻辑回归为最佳分类算法
classifier = classfier_model(classifier_ag=NuSVC())


# 用最佳分类器预测待测文本
def predict_page(page):
    print(page)
    data = build_page(page)
    pred = classifier.classify_many(data)
    return pred


pos = 0
neg = 0
# 分段预测文本
with open('./20.3.10-20.6.json', 'r', encoding='utf8')as rd:
    json_data = json.load(rd)
    length = len(json_data)
    for i in range(0, length):
        page = json_data[str(i)]
        re = predict_page(page)
        if re[0] == 'pos':
            pos = pos + 1
        else:
            neg = neg + 1
    print("总计有", length, "条数据")
    print("积极的评论有", pos, "条")
    print("消极的评论有", neg, "条")

print(predict_page("太他妈难了，该怎么评论啊"))
