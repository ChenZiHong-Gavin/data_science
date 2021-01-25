import oneWord
# 把词语（双字）作为搭配，并通过卡方统计，选取排名前n的词语
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures


def bigram(words, score_fn=BigramAssocMeasures.chi_sq, n=20):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    # 使用卡方统计的方法，选择排名前1000的词语
    newBigrams = [u + v for (u, v) in bigrams]
    return oneWord.bag_of_words(newBigrams)


# print(bigram(text(), score_fn=BigramAssocMeasures.chi_sq, n=20))
