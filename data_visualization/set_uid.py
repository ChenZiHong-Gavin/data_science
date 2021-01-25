# coding: utf-8

import json


def read_json(file_name):
    json_file = open(file_name, encoding='UTF-8')
    weibo_str = json_file.read()
    json_file.close()
    json_obj = json.loads(weibo_str)
    return json_obj


weibo_json = read_json("weibo.json")
uid = 1
for weibo in weibo_json['weibo']:
    for comments in weibo['comment']:
        for oneComment in comments:
            oneComment['uid'] = uid
            uid += 1

out_json_str = json.dumps(weibo_json, ensure_ascii=False)
out_file = open("WeiboUid.json", "w", encoding='UTF-8')
out_file.write(out_json_str)
out_file.close()
print("123")
