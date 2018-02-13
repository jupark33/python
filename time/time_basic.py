from datetime import datetime, timedelta

class Time_basic(object):
    def __init__(self):
        self

    def cal_date(self):
        print('cal_date')
        # 오늘부터 5일을 더하고 5시간을 뺀다.
        print(datetime.now() + timedelta(days=5, hours=-5))

        today = datetime.now()
        yesterday = today + timedelta(days=1)

        # 오늘 - 어제
        print('today - yesterday : ')
        print(today - yesterday)

        # 오늘날짜에서 어제 날짜 를 빼고 차이나는 날짜 수
        print('(today-yesterday).days : ')
        print((today - yesterday).days)

    def comp_date(self):
        today_1 = datetime.now()
        today_2 = datetime.now()

        # 오늘 - 오늘
        print('today_1 - today_2 : ')
        print(today_1 - today_2)

if __name__ == '__main__':
    tb = Time_basic()
    # tb.cal_date()
    tb.comp_date()
