# 스케줄러 2번째 버전

from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime

class Scheduler(object):
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.job_id = ''
    # 클래스 종료 시 모든 job 종료
    def __del__(self):
        self.shutdown()
    # 모든 job 종료
    def shutdown(self):
        self.sched.shutdown()
    # 특정job종료
    def kill_scheduler(self, job_id):
        try:
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            str_now = getNow()
            print("[%s] fail to stop scheduler: %s" % str_now, err)
            return
    # Task
    def task(self, type, job_id):
        # print("%s task id[%s] : %d" % (type, job_id, time.localtime().tm_sec))
        str_now = getNow()
        print("[%s] %s task id[%s]" % (str_now, type, job_id))

    # 스케줄러생성
    def scheduler(self, type, job_id):
        str_now = getNow()
        print("[%s] Scheduler Start" % str_now, type)
        self.sched.add_job(self.task, type, day_of_week='mon-fri', hour='0-23', second='*/2', id=job_id, args=(type, job_id))

class Scheduler_Killer(object):
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.job_id = ''

    # 클래스 종료 시 모든 job 종료
    def __del__(self):
        self.shutdown()

    # 모든 job 종료
    def shutdown(self):
        self.sched.shutdown()

    # Task : 작업 스케줄러의 모든 job을 kill
    def task(self, type, job_id, object):
        global isKilled
        str_now = getNow()
        object.shutdown()
        isKilled = True
        print("[%s] Scheduler is shutdowned " % str_now)

    # 스케줄러 생성 ( 월-금 매일 10:00 가 되면, 작업 스케줄러의 모든 job을 kill )
    def scheduler(self, type, job_id, object, hour, minute):
        str_now = getNow()
        print("[%s] %s Kill Scheduler Start" % (str_now, type))
        self.sched.add_job(self.task, type, day_of_week='mon-fri', hour=hour, minute=minute, id=job_id, args=(type, job_id, object))

def getNow():
    now = time.localtime()
    str_now = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return str_now

if __name__ == '__main__':
    # 작업 스케줄러
    scheduler = Scheduler()
    scheduler.scheduler("cron", "1")

    # 작업 스케줄러를 종료하기 위한 스케줄러
    kill_scheduler = Scheduler_Killer()
    # scheduler.scheduler_all_kill("cron", "2")
    kill_scheduler.scheduler("cron", "kill", scheduler, 13, 36)

    # 작업 스케줄러 Kill 되었는지
    isKilled = False

    # 중요 : 무한 루프가 없으면, 메인 스레드가 종료되면서, task 도 종료되므로 아무것도 출력되지 않는다.
    while True:
        str_now = getNow()

        print("[%s] --- main thread ---" % str_now)
        time.sleep(1)
        if isKilled == True:
            break

    str_now = getNow()
    print("[%s] --- exit main thread ---" % str_now)
