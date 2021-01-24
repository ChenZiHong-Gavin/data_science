import csv


def get_dict():
    result = {}
    with open('dictionary/情感词汇本体.csv', encoding='utf-8') as csv_file:
        spam_reader = csv.reader(csv_file)
        for row in spam_reader:
            if row[2].isdecimal():
                if not row[4] in result:
                    result[row[4]] = {}
                result[row[4]][row[0]] = row[5]

    return result


if __name__ == '__main__':
    get_dict()
