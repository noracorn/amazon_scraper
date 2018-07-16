# -*- coding: utf-8 -*-
import sys
import time


def main(argv=sys.argv[1:]):

    if len(argv) == 0:
        chop_data(u"対象ファイルを指定してください。")

    if len(argv) == 1:
        # セラーファイルからASINをぶっこ抜く
        file_name = argv[0]
        get_asin_from_seller(file_name)


def get_asin_from_seller(file_name):
    file = open(file_name, 'r')
    data_list = []
    for line in file:
        if chop_data(line) not in data_list:
            if chop_data(line).count("/dp/"):
                data_list.append(replace_asin(chop_data(line)))
        else:
            print(chop_data(line))
    file.close

    output_file = open("asin_from_seller.txt", 'w')
    for data in data_list:
        output_file.write("{0}\n".format(data))
    output_file.close()


def replace_asin(data):
    return data[data.index("/dp/") + 4: data.index("/dp/") + 4 + data[data.index("/dp/") + 4:].index("/")]


def chop_data(data):
    data = data.replace("\n", "")
    return data


if __name__ == '__main__':
    main()
