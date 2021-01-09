import pypinyin


def set_pinyin(words):
    pinyin = pypinyin.lazy_pinyin(words)
    return pinyin

if __name__ == '__main__':
    print(set_pinyin)