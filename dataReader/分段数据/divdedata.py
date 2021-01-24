import json

num1 = 0
num2 = 0
num3 = 0
num4 = 0
with open('./人民日报微博及评论.json', 'r', encoding='utf8')as fp:
    total_data = json.load(fp)
    user = total_data['user']
    wei_bo = total_data['weibo']
    dic1 = {}
    dic2 = {}
    dic3 = {}
    dic4 = {}
    for weibo in wei_bo:
        content = weibo['content']
        time = weibo['publish_time']
        if (time > '2019-12-08') and (time < '2020-01-22'):
            dic1[str(num1)] = content
            num1 = num1+1
        comments = weibo['comment']
        for items in comments:
            for item in items:
                publish_time = item['publish_time']
                con = item['content']
                if (publish_time > '2019-12-08') and (publish_time < '2020-01-22'):
                    dic1[num1] = con
                    num1 = num1+1
    with open('19.12.8-20.1.22.json', 'a', encoding='utf8')as wp1:
        json.dump(dic1, wp1, ensure_ascii=False)

        for weibo in wei_bo:
            content = weibo['content']
            time = weibo['publish_time']
            if (time > '2020-01-23') and (time < '2020-02-07'):
                dic2[str(num2)] = content
                num2 = num2 + 1
            comments = weibo['comment']
            for items in comments:
                for item in items:
                    publish_time = item['publish_time']
                    con = item['content']
                    if (time > '2020-01-23') and (time < '2020-02-07'):
                        dic2[num2] = con
                        num2 = num2 + 1
        with open('20.1.23-20.2.7.json', 'a', encoding='utf8')as wp2:
            json.dump(dic2, wp2, ensure_ascii=False)

        for weibo in wei_bo:
            content = weibo['content']
            time = weibo['publish_time']
            if (time > '2020-02-10') and (time < '2020-02-23'):
                dic3[str(num3)] = content
                num3 = num3 + 1
            comments = weibo['comment']
            for items in comments:
                for item in items:
                    publish_time = item['publish_time']
                    con = item['content']
                    if (time > '2020-02-10') and (time < '2020-02-23'):
                        dic3[num3] = con
                        num3 = num3 + 1
        with open('20.2.10-20.2.23.json', 'a', encoding='utf8')as wp3:
            json.dump(dic3, wp3, ensure_ascii=False)

        for weibo in wei_bo:
            content = weibo['content']
            time = weibo['publish_time']
            if (time > '2020-03-10') and (time < '2020-06'):
                dic4[str(num4)] = content
                num4 = num4 + 1
            comments = weibo['comment']
            for items in comments:
                for item in items:
                    publish_time = item['publish_time']
                    con = item['content']
                    if (time > '2020-03-10') and (time < '2020-06'):
                        dic4[num4] = con
                        num4 = num4 + 1
        with open('20.3.10-20.6.json', 'a', encoding='utf8')as wp4:
            json.dump(dic4, wp4, ensure_ascii=False)