# 把单个字和词语一起作为特征
from nltk import BigramAssocMeasures, BigramCollocationFinder

from oneWord import bag_of_words


def bigram_words(words, score_fn=BigramAssocMeasures.chi_sq, n=20):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    newBigrams = [u + v for (u, v) in bigrams]
    a = bag_of_words(words)
    b = bag_of_words(newBigrams)
    a.update(b)  # 把字典b合并到字典a中
    return a  # 所有单个字和双个字一起作为特征


# print(bigram_words(text(), score_fn=BigramAssocMeasures.chi_sq, n=10))
