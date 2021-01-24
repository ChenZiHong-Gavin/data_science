import _thread
import codecs  # 用来存储爬取到的信息
import math
import threading
import time

from pybloom_live import ScalableBloomFilter  # 用于URL去重的
import requests  # 用于发起请求，获取网页信息
import json  # 处理json格式的数据
from bs4 import BeautifulSoup as bs  # 用于数据抽取
import re  # 正则语言类库


def getdetailpagebybs(url):
    detail = {}  # 创建一个字典，存放URL、title、newstime等信息
    detail["url"] = url  # 将URL时间存入detail字典中的相应键值中
    print("s", end="")
    page = None
    i = 0
    while not page:
        try:
            page = requests.get(url, timeout=3).content
        except Exception:
            i += 1
            print(" " + str(i) + " ", end="")
            if i == 3:
                return None

    # 使用requests.get方法获取网页代码，由于bs4可以自动解码URL的编码，所以此处不需要decode
    print("r", end="")
    html = None
    try:
        html = bs(page, "lxml")  # 使用lxml解析器
    except TypeError:
        print(page)
        return None
    title = html.find(class_="main-title")  # 获取新闻网页中的title信息，此处网页中只有一个“class=main-title”，所以使用find即可
    if title == None:
        print(url, end="")
        return None
    # print(title.text)  # 展示新闻标题
    detail["title"] = title.text  # 将新闻标题以文本形式存入detail字典中的相应键值中
    artibody = html.find(class_="article")  # 使用find方法，获取新闻网页中的article信息
    # print(artibody.text)
    detail["artibody"] = artibody.text  # 。。。。。。。
    date_source = html.find(class_="date-source")  # 使用find方法，获取新闻网页中的date-source信息
    # 由于不同的新闻详情页之间使用了不同的标签元素，直接抽取可能会报错，所以此处使用判断语句来进行区分爬取
    if date_source.a:  # 判断date-source节点中是否包含有'a'元素
        # print(date_source.span.text)
        detail["newstime"] = date_source.span.text  # 抽取'span'标签中时间信息
        # print(date_source.a.text)
        detail["newsfrom"] = date_source.a.text  # 抽取'a'标签中新闻来源信息
    else:
        # print(date_source("span")[0].text)
        detail["newstime"] = date_source("span")[0].text  # 抽取'span'标签中包含的时间信息
        # print(date_source("span")[1].text)
        detail["newsfrom"] = date_source("span")[1].text  # 抽取'span'标签中包含的新闻来源信息
    return detail  # 函数返回值为存放抽取信息的字典


def save_news(data, new):
    fp = codecs.open('D:/sinaNews/' + new + '.json', 'a+', 'utf-8')
    fp.write(json.dumps(data, ensure_ascii=False))
    fp.close()


def is_interesting(text):
    if "疫" in text or "病毒" in text or "新冠" in text or "肺炎" in text or "covid" in text:
        return True
    return False


def get_news(time_stamp):
    time_local = time.localtime(time_stamp)
    # 转换成新的时间格式(2016-05-05)
    dt = time.strftime("%Y-%m-%d", time_local)

    # 使用ScalableBloomFilter模块，对获取的URL进行去重处理
    url_bloom_filter = ScalableBloomFilter(initial_capacity=100, error_rate=0.001,
                                           mode=ScalableBloomFilter.LARGE_SET_GROWTH)
    page = 1  # 设置爬虫初始爬取的页码
    error_url = set()  # 创建集合，用于存放出错的URL链接
    # 使用BeautifulSoup抽取模块和存储模块
    # 设置爬取页面的上限，
    page_num = 10000

    news_result = []
    thresds = []
    while page <= page_num:
        # 以API为index开始获取url列表
        print(" sp ", end="")
        data = requests.get(
            "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&etime={}&stime={}&ctime={}&date={}&page={}".format(
                time_stamp, time_stamp + 86400, time_stamp + 86400, dt, page))  # 拼接URL，并获取索引页面信息
        print(" rp ", end="")
        if data.status_code == 200:  # 当请求页面返回200（代表正确）时，获取网页数据
            # 将获取的数据json化
            data_json = json.loads(data.content)
            if page_num == 10000:
                page_num = math.ceil(int(data_json.get("result").get("total")) / 50)
            news = data_json.get("result").get("data")  # 获取result节点下data节点中的数据，此数据为新闻详情页的信息
            # 从新闻详情页信息列表news中，使用for循环遍历每一个新闻详情页的信息
            for new in news:
                # 查重，从new中提取URL，并利用ScalableBloomFilter查重
                if new["url"] not in url_bloom_filter:
                    url_bloom_filter.add(new["url"])  # 将爬取过的URL放入urlbloomfilter中
                    try:
                        if is_interesting(new['title']):
                            thread = LoadPage(new["url"], news_result)
                            thresds.append(thread)
                            thread.start()
                            # print(new)
                            # 抽取模块使用bs4
                            # detail = getdetailpagebybs(new["url"])
                            # 存储模块 保存到txt
                            # news_result.append(detail)
                            # save_news(detail,
                            #           new['docid'][-7:])
                    except Exception as e:
                        error_url.add(new["url"])  # 将未能正常爬取的URL存入到集合error_url中
            page += 1  # 页码自加1
    for thread in thresds:
        thread.join()
    save_news(news_result, dt)


class LoadPage(threading.Thread):
    def __init__(self, url, news):
        threading.Thread.__init__(self)
        self.url = url
        self.news = news

    def run(self):
        self.news.append(getdetailpagebybs(self.url))


if __name__ == '__main__':
    start_date = "2020-03-04"
    end_date = "2020-07-01"

    start_stamp = int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))
    end_stamp = int(time.mktime(time.strptime(end_date, "%Y-%m-%d")))

    time_now = start_stamp

    while time_now < end_stamp:
        print()
        get_news(time_now)
        # _thread.start_new_thread(get_news, (time_now,))
        time_now += 86400
