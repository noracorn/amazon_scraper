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
    asin = argv[1]
    get_price(market, asin)


def get_price(market, asin):
    try:
        url = urls[market].format(asin)
        html = req.urlopen(url)
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


def get_price_pattern1(soup):
    outprice = soup.select("#priceblock_ourprice")
    if outprice:
        price = parse_price(outprice[0].string)

    shipping = soup.select(".shipping3P")
    if shipping:
        shipping = parse_price(shipping[0].string)
        if shipping:
            price = str(int(price) + int(shipping))

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


def parse_price(price):
    price = price.replace(',', '')
    price = price.replace('￥', '')
    price = price.replace(' ', '')
    price = price.replace('+', '')
    price = price.replace('\n', '')

    if not price.isdecimal():
        for index, moji in enumerate(price):
            if not moji.isdecimal():
                break
        price = price[0:index]

    return price


if __name__ == '__main__':
    main()