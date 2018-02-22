import urllib3
from xml.dom import minidom
from bs4 import BeautifulSoup

url = 'http://asp1.krx.co.kr/servlet/krx.asp.XMLSise?code=004770'

http = urllib3.PoolManager()
r = http.request('GET', url)

# print(r.data)

soup = BeautifulSoup(r.data, "lxml")

# print('--stockprice--')
# stockprice = soup.findAll('stockprice')
# print(stockprice)

print('--dailystock--')
dailystocks = soup.findAll('dailystock')
print(dailystocks)
print('date   volume     start    endprice')
for ds in dailystocks:
    print(ds['day_date'], ds['day_volume'], ds['day_start'], ds['day_endprice'])
