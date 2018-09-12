import win32com.client
import pythoncom
import operator

class XASessionEventHandler:
    login_state = 0

    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인 성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인 실패")

class XAQueryEventHandlerT1452:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT1452.query_state = 1

class Stock:
    # 종목명
    def setName(self, hname):
        self.hname = hname

    # 종목코드
    def setShcode(self, shcode):
        self.shcode = shcode

    # 현재가
    def setPrice(self, price):
        self.price = price

    # 전일대비
    def setChane(self, change):
        self.change = change

    # 당일누적거래량
    def setVolume(self, volume):
        self.volume = volume

    # 전일대비
    def setChange(self, change):
        self.change = change

    # 전일거래량
    def setJnivolume(self, jnivolume):
        self.jnivolume = jnivolume

instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)

#id = "아이디"
#passwd = "비밀번호"
#cert_passwd = "공인인증서"

instXASession.ConnectServer("hts.ebestsec.co.kr", 20001)
instXASession.Login(id, passwd, cert_passwd, 0, 0)

while XASessionEventHandler.login_state == 0:
    pythoncom.PumpWaitingMessages()

num_account = instXASession.GetAccountListCount()
for i in range(num_account):
    account = instXASession.GetAccountList(i)
    print(account)

#----------
# T1452
# shcode : 단축코드
#----------
instXAQueryT1452 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT1452)
instXAQueryT1452.ResFileName = "C:\\eBest\\xingAPI\\Res\\t1452.res"

instXAQueryT1452.SetFieldData("t1452InBlock", "gubun", 0, 1)
instXAQueryT1452.Request(0)

while instXAQueryT1452.query_state == 0:
    pythoncom.PumpWaitingMessages()

count = instXAQueryT1452.GetBlockCount("t1452OutBlock1")
print('전체 갯수 : ' + str(count))  # 2018.09.10 : 1489

# 거래량 높은 40개 종목을, 종목명 순으로 정렬하여 출력
# stock_list = []
stock_list = list()

for i in range(count):
    hname = instXAQueryT1452.GetFieldData("t1452OutBlock1", "hname", i)         #종목명
    shcode = instXAQueryT1452.GetFieldData("t1452OutBlock1", "shcode", i)       #종목코드
    price = instXAQueryT1452.GetFieldData("t1452OutBlock1", "price", i)         #현재가
    volume = instXAQueryT1452.GetFieldData("t1452OutBlock1", "volume", i)       #당일누적거래량
    change = instXAQueryT1452.GetFieldData("t1452OutBlock1", "change", i)       #전일대비
    jnivolume = instXAQueryT1452.GetFieldData("t1452OutBlock1", "jnivolume", i) #전일거래량

    i_price = int(price)

    aStock = Stock()
    aStock.setName(hname)
    aStock.setShcode(shcode)
    # print('name : ' + hname)
    aStock.setPrice(i_price)
    aStock.setVolume(volume)
    aStock.setChange(change)
    aStock.setJnivolume(jnivolume)

    stock_list.append(aStock)
    # print('name of astock : ' + aStock.getName())
    # aStock = None

# item_list.sort()
# print('len item : ' + str(len(stock_list)))

stock_list.sort(key=operator.attrgetter('volume'))
for stock in stock_list:
    # print(stock.hname + ", [종목코드]" + stock.shcode + ", [가격]" + str(stock.price) + ", [전일거래량]" + str(stock.jnivolume) + ", [전일대비]" + str(stock.change) + ", [누적거래량]" + str(stock.volume))
    print("[종목명]" + stock.hname + ", [종목코드]" + stock.shcode + ", [가격]" + str(stock.price) + ", [당일누적거래량]" + str(stock.volume))
