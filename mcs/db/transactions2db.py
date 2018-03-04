from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
import urllib3
from xml.dom import minidom
from bs4 import BeautifulSoup

from db_engine import Base, Transaction, engine
from kr.co.lop.mcs.util.StringUtil import strCommaToInt, change_hour_minute, timestamp_to_time
from datetime import datetime, timedelta
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class Processor_Transactions(object):
    
    def __init__(self):
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
    
    def tran_2_db(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        url = 'https://api.korbit.co.kr/v1/transactions'
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        
#         soup = BeautifulSoup(r.data)
#         soup = BeautifulSoup(r)
        soup = json.loads(r.data.decode('utf-8'))
        
        for each in soup:
#             print('each : ' + str(each))
            dt_deal = timestamp_to_time(each['timestamp'])
            tid = each['tid']
            price = each['price']
            amount = each['amount']
#             print('dt_deal : ' + str(dt_deal) + ', tid : ' + tid + ', price : ' + price + ', amount : ' + amount)
            
            new_transaction = Transaction(tid=tid, price=price, amount=amount, dt_deal=dt_deal, c_type=1)
            
            exist = self.isExistTransactionDate(new_transaction.dt_deal)
            if exist == True:
                print(str(dt_deal) + '은 이미 존재함')
            else:
                print(str(dt_deal) + '은 신규임')
                self.session.add(new_transaction)
        
        self.session.commit()

    # 이미 존재하는 날짜+시간 인지 체크 (True : 이미 존재, False : 존재 하지 않음)
    def isExistTransactionDate(self, target_dt):
        result = False
        for instance in self.session.query(Transaction):
            if instance.dt_deal == target_dt:
                result = True
                break
        return result
        
if __name__ == '__main__':
    p_transactions = Processor_Transactions()
    p_transactions.tran_2_db()
