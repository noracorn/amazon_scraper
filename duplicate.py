# -*- coding: utf-8 -*-
import sys
import time
from urllib.error import HTTPError


def main(argv=sys.argv[1:]):

    if len(argv) == 0:
        chop_data(u"対象ファイルAを指定してください。")

    if len(argv) == 1:
        # 1ファイルの場合は、そのファイルの中での重複
        file_name = argv[0]
        search_duplicate_one_file(file_name)

    elif len(argv) == 2:
        # 2ファイルの場合は、1つ目のファイルから、2つ目のファイルに含まれているものを出す。
        file_name_a = argv[0]
        file_name_b = argv[1]
        search_duplicate_two_file(file_name_a, file_name_b)

    elif len(argv) == 3:
        # 3番目の引数を渡すと、重複していないものを出す。
        file_name_a = argv[0]
        file_name_b = argv[1]
        search_not_included_data_two_file(file_name_a, file_name_b)


def search_duplicate_one_file(file_name):
    file = open(file_name, 'r')
    data_list = []
    for line in file:
        if line not in data_list:
            data_list.append(chop_data(line))
        else:
            print(chop_data(line))
    file.close


def search_duplicate_two_file(file_name_a, file_name_b):
    file_a = open(file_name_a, 'r')
    file_b = open(file_name_b, 'r')
    data_list = [chop_data(line) for line in file_a]
    for line in file_b:
        if chop_data(line) in data_list:
            print(chop_data(line))
    file_a.close
    file_b.close


def search_not_included_data_two_file(file_name_a, file_name_b):
    file_a = open(file_name_a, 'r')
    file_b = open(file_name_b, 'r')
    data_list_a = [chop_data(line) for line in file_a]
    data_list_b = [chop_data(line) for line in file_b]

    result = set(data_list_b) - set(data_list_a)

    for data in result:
        print(data)

    file_a.close
    file_b.close



def chop_data(data):
    data = data.replace("\n", "")
    return data


if __name__ == '__main__':
    main()
