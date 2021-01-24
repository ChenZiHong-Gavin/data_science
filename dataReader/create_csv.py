import csv

from sentiDict.sentiment import Sentiment
from set_uid import read_json
import jieba


def create_csv_for_mark():
    weibo_json = read_json("WeiboUid.json")

    with open('weibo.csv', 'w', encoding='UTF-8') as csv_file:
        spam_writer = csv.writer(csv_file)
        for weibo in weibo_json['weibo']:
            for comments in weibo['comment']:
                for oneComment in comments:
                    spam_writer.writerow([oneComment['uid'], oneComment['content']])


def create_csv_for_word_cloud():
    weibo_json = read_json("WeiboUid.json")
    word_cloud_set = {}

    for weibo in weibo_json['weibo']:
        for comments in weibo['comment']:
            for oneComment in comments:
                for word in jieba.lcut(oneComment['content']):
                    if not word in word_cloud_set:
                        word_cloud_set[word] = 0
                    word_cloud_set[word] += 1

    stop_word = get_stop_word()

    with open('wordCloud.csv', 'w', encoding='UTF-8') as csv_file:
        spam_writer = csv.writer(csv_file, delimiter=';')
        for word, weight in sorted(word_cloud_set.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
            if not word in stop_word:
                spam_writer.writerow([word, weight])


def get_stop_word():
    stop_word = set()
    with open('stop_word.txt', encoding='utf-8') as stop_word_file:
        for word in stop_word_file.read().split('\n'):
            stop_word.add(word)
    stop_word.add(" ")
    return stop_word


def create_for_graph():
    weibo_json = read_json("WeiboUid.json")
    data_out = {}
    senti_cal = Sentiment()

    for weibo in weibo_json['weibo']:
        publish_time = weibo['publish_time'].split(" ")[0]
        if publish_time == '2021-01-20':
            continue
        for comments in weibo['comment']:
            for oneComment in comments:
                senti_result = senti_cal.sentiment_calculate(oneComment['content'])
                if 'NN' not in senti_result:
                    continue
                if publish_time not in data_out:
                    print(publish_time)
                    data_out[publish_time] = senti_result
                else:
                    for senti in data_out[publish_time]:
                        data_out[publish_time][senti] += senti_result[senti]

    with open('senti_cal.csv', 'w', encoding='UTF-8') as csv_file:
        spam_writer = csv.writer(csv_file, delimiter=',')
        spam_writer.writerow(["senti", "date", "weight"])
        for date, senti_all in data_out.items():
            for senti, weight in senti_all.items():
                spam_writer.writerow([senti, date, weight])


if __name__ == '__main__':
    create_for_graph()
