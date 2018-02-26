from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
import urllib3
from xml.dom import minidom
from bs4 import BeautifulSoup

from db_engine import Base, Stock_info, Volume, engine
from StringUtil import strCommaToInt, change_hour_minute
from datetime import datetime, timedelta

def get_basic_inf():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    result = session.query(Stock_info).all()
    print(result)

    for info in session.query(Stock_info).all():
        print('no:' + str(info.no) + ', st_code:' + info.st_code + ', st_name:' + info.st_name)

def get_volume_n_price(st_code):
    url = 'http://asp1.krx.co.kr/servlet/krx.asp.XMLSise?code=' + st_code
    http = urllib3.PoolManager()
    r = http.request('GET', url)

    soup = BeautifulSoup(r.data, "lxml")

    # print('--dailystock--')  # 디버깅 용도
    dailystocks = soup.findAll('dailystock')
    # print(dailystocks) # 디버깅 용도

    print('st_code : ' + st_code)
    print('date   volume     start    endprice')
    for ds in dailystocks:
        # print(ds['day_date'], ds['day_volume'], ds['day_start'], ds['day_endprice'])
        new_volume = Volume(st_code=st_code, dt_date=ds['day_date'], volume=ds['day_volume'])
        print(new_volume.st_code + ', ' + new_volume.dt_date + ', ' + new_volume.volume)

class Processor_Volume(object):

    def __init__(self):
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def krx_2_db(self, st_code):
        url = 'http://asp1.krx.co.kr/servlet/krx.asp.XMLSise?code=' + st_code
        http = urllib3.PoolManager()
        r = http.request('GET', url)

        soup = BeautifulSoup(r.data, "lxml")

        # print('--dailystock--')  # 디버깅 용도
        dailystocks = soup.findAll('dailystock')
        # print(dailystocks) # 디버깅 용도

        print('st_code : ' + st_code)
        for ds in dailystocks:
            # print(ds['day_date'], ds['day_volume'], ds['day_start'], ds['day_endprice'])
            str_date = ds['day_date']
            date = datetime.strptime(str_date, '%y/%m/%d')

            date = change_hour_minute(date, 23, 59)
            new_volume = Volume(st_code=st_code, dt_date=date, volume=strCommaToInt(ds['day_volume']))
            # print(new_volume.st_code + ', ' + str(new_volume.dt_date) + ', ' + str(new_volume.volume))

            exist = self.isExistVolumeDate(new_volume.dt_date)
            if exist == True:
                print(str(new_volume.dt_date) + '은 이미 존재함')
            else:
                print(str(new_volume.dt_date) + '은 신규임')
                self.session.add(new_volume)

            # self.session.add(new_volume)
        self.session.commit()


            # date     volume     start    endprice
            # 18/02/23 10,303,817 4,525    4,680
            # 18/02/22 23,797,843 4,580    4,530
            # 18/02/21 73,431,572 4,250 4,650
            # 18/02/20 47,410,354 3,300 4,290
            # 18/02/19 7,494,844 3,220 3,300
            # 18/02/14 7,396,193 3,150 3,080
            # 18/02/13 9,180,467 2,850 3,070
            # 18/02/12 415,465 2,805 2,805
            # 18/02/09 316,883 2,730 2,790
            # 18/02/08 470,086 2,725 2,790

    # Volume 테이블 조회
    def query_volume(self):
        for instance in self.session.query(Volume):
            print(instance.st_code + ', ' + str(instance.dt_date) + ', ' + str(instance.volume))

    # 이미 존재하는 날짜+시간 인지 체크 (True : 이미 존재, False : 존재 하지 않음)
    def isExistVolumeDate(self, target_dt):
        result = False
        for instance in self.session.query(Volume):
            if instance.dt_date == target_dt:
                result = True
                break
        return result
if __name__ == '__main__':
    # get_basic_inf()
    # get_volume_n_price('004770')
    p_volume = Processor_Volume()
    p_volume.krx_2_db('004770')
    # p_volume.query_volume()
