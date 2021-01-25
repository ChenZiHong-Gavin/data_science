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