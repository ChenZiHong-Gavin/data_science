# 单个字作为特征
def bag_of_words(words):
    return dict([(word, True) for word in words])

# print(bag_of_words(text()))
