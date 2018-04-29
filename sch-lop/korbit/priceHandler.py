#-*- coding: utf-8 -*-
from util.listUtil import get_av
import requests
import urllib3
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from util.StringUtil import change_hour_minute, print_log, timestamp_to_time, getNow
from util.slackUtil import postMsg, web_hook_sendMsg
import enum
from korbit.common import Type_Coin, Name_Coin

class PriceHandler(object):

    def __init__(self):
        self.btc_krw = 0
        self.etc_krw = 0
        self.eth_krw = 0
        self.xrp_krw = 0
        self.bch_krw = 0
        self.price_total = ''

    def run(self):
        for key in Type_Coin:
            msg = self.getPrice(key, key.value)
            self.price_total += msg

        print_log('\n' + self.price_total)
        web_hook_sendMsg('\n' + self.price_total)

    def getName(self, key):
        return Name_Coin[key].value

    def getPrice(self, key, type_coin):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        url = 'https://api.korbit.co.kr/v1/ticker/detailed'
        v_fields = {'currency_pair' : type_coin}
        http = urllib3.PoolManager()
        r = http.request('GET', url, fields=v_fields)
        r_json = json.loads(r.data.decode('utf-8'))

        # {'timestamp': 1524983980880, 'last': '10170000', 'bid': '10169500', 'ask': '10170000', 'low': '9890000',
        #  'high': '10260000', 'volume': '1049.539082211128927493', 'change': '177500', 'changePercent': '1.78'}
        # print_log('result : ' + str(r_json))

        c_name = str(self.getName(type_coin))
        # print_log(val)

        msg = str(r_json)
        msg = r_json['last']
        price = int(msg)
        s_price = format(price, ",")
        msg = c_name + ' 가격 : ' + s_price + '\n'

        return msg
        # print_log(msg)
        # self.price_total += msg
        # web_hook_sendMsg(msg)
        # print_log('type_coin : ' + str(type_coin) + 'value : ' + self.getName(type_coin))

if __name__ == '__main__':
    ph = PriceHandler()
    ph.run()
    # for key in Type_Coin:
    #     print(key.value)
