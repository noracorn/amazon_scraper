# -*- coding: utf-8 -*-
import sys
import time
import urllib.request as req
from bs4 import BeautifulSoup
from urllib.error import HTTPError

urls = {
    'jp': "https://www.amazon.co.jp/dp/{0}",
    'us': "https://www.amazon.com/dp/{0}"
}


def main(argv=sys.argv[1:]):

    if argv[0] not in urls.keys():
        print(u"マーケットを指定してください(jp, us)")

    if len(argv) != 2:
        print(u"引数が足りません。マーケット、ASIN")

    market = argv[0]
    asin_file = argv[1]

    file = open(asin_file, 'r')
    for line in file:
        asin = line.replace('\n', '')
        price = get_price(market, asin)
        write_file(asin, price)


def get_price(market, asin):
    try:
        url = urls[market].format(asin)
        print("start")
        time.sleep(1)
        html = req.urlopen(url)
        print("end")
        soup = BeautifulSoup(html, 'html.parser')

        price = get_price_pattern1(soup)
        if not price:
            price = get_price_pattern2(soup)
        if not price:
            price = get_price_pattern3(soup)
        print(price)
        time.sleep(1)
        return price
    except HTTPError as e:
        if e.code == 503:
            time.sleep(5)
            get_price(market, asin)
    except Exception as e:
        time.sleep(5)
        get_price(market, asin)


def get_price_pattern1(soup):
    outprice = soup.select("#priceblock_ourprice")
    if outprice:
        price = parse_price(outprice[0].string)
        return price


def get_price_pattern2(soup):
    outprice = soup.select("#MediaMatrix .a-color-base .a-size-base")
    if outprice:
        price = parse_price(outprice[0].string)
        return price


def get_price_pattern3(soup):
    outprice = soup.select("#olp_feature_div .a-color-price")
    if outprice:
        price = parse_price(outprice[0].string)
        return price


# def write_file(asin, price):
#     file = open('output.txt', 'a')
#     file.write("{0}\n".format(",".join([asin, price])))
#     file.close
def write_file(asin, price):
    file = open('output.txt', 'a')
    if price:
        file.write("{0}\n".format(price))
    else:
        file.write(u"在庫切れ\n")
    file.close


def parse_price(price):
    price = price.replace(',', '')
    price = price.replace('￥', '')
    price = price.replace(' ', '')
    price = price.replace('\n', '')
    return price



if __name__ == '__main__':
    main()
