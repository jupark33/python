import enum

class Type_Coin(enum.Enum):
    btc_krw = 'btc_krw'
    etc_krw = 'etc_krw'
    eth_krw = 'eth_krw'
    xrp_krw = 'xrp_krw'
    bch_krw = 'bch_krw'
    ltc_krw = 'ltc_krw'

class Name_Coin(enum.Enum):
    btc_krw = '비트코인'
    etc_krw = '이러디움 클래식'
    eth_krw = '이러디움'
    xrp_krw = '리플'
    bch_krw = '비트코인 캐쉬'
    ltc_krw = '라이트 코인'

if __name__ == '__main__':
    for key in Type_Coin:
        print(key.value)
