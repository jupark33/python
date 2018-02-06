# https://www.clien.net/service/board/lecture/9328705
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import time

class Scheduler(object):
    # 클래스 생성 시 스케줄러 데몬을 생성
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.job_id = ''
    # 클래스 종료 시, 모든 job들을 종료
    def __del__(self):
        self.shutdown()
    # 모든 job들을 종료
    def shutdown(self):
        self.sched.shutdown()
    # 특정 job을 종료
    def kill_scheduler(self, job_id):
        try:
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            print("fail to stop scheduler: %s" % err)
            return
    def hello(self, type, job_id):
        print("%s scheduler process_id[%s] : %d" %(type, job_id, time.localtime().tm_sec))
    # 스케줄러가 실행되면서 hello를 실행시키는 스레드 생성
    # 다음 함수는 type 인수 값에 따라 cron과 interval 형식으로 지정
    # 인수값이 cron일 경우, 날짜, 요일, 시간, 분, 초 등의 형식으로 지정하여,
    # 특정 시각에 실행되도록 함. (cron 과 동일)
    # interval의 경우, 설정된 시간을 간격으로 일정하게 실행 가능
    def scheduler(self, type, job_id):
        print("%s Scheduler Start" % type)
        if type == 'interval':
            self.sched.add_job(self.hello, type, seconds=10, id=job_id, args=(type, job_id))
        elif type == 'cron':
            self.sched.add_job(self.hello, type, day_of_week='mon-fri', hour='0-23', second='*/2', id=job_id, args=(type, job_id))

if __name__ == '__main__':
    scheduler = Scheduler()
    # cron 스케줄러를 실행시키며, job_id는 "1", 10초 간격으로 실행됨  
    scheduler.scheduler('cron', "1")
    # interval 스케줄러를 실행시키며, job_id 는 "2" 2초 간격으로 실행됨  
    scheduler.scheduler('interval', "2")
    count = 0
    while True:
        print("Running main process.............")
        time.sleep(1)
        count += 1
        if count == 10:
            scheduler.kill_scheduler("1")
            print("##### kill cron schedule #####")
        elif count == 30:
            scheduler.kill_scheduler("2")
            print("##### kill interval schedule #####")



