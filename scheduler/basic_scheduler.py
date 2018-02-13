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
            print("fail to stop scheduler: %s" % err)
            return
    # Task
    def task(self, type, job_id):
        # print("%s task id[%s] : %d" % (type, job_id, time.localtime().tm_sec))
        now = time.localtime()

        str_now = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        print("%s task id[%s] : %sg" % (type, job_id, str_now))
    # 스케줄러생성
    def scheduler(self, type, job_id):
        print("%s Scheduler Start" % type)
        self.sched.add_job(self.task, type, day_of_week='mon-fri', hour='0-23', second='*/2', id=job_id, args=(type, job_id))

    # 스케줄러 생성 ( 월-금 매일 10:00 가 되면, 모든 job을 kill 함
    def kill_scheduler(self, type, job_id):
        print("%s Kill Scheduler Start" % type)
        

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.scheduler("cron", "1")
    count = 0

    # 중요 : 무한 루프가 없으면, 메인 스레드가 종료되면서, task 도 종료되므로 아무것도 출력되지 않는다.
    while True:
        print("--- main thread ---")
        time.sleep(1)
        count = count + 1
        if count == 10:
            scheduler.kill_scheduler("1")
            print("--- kill cron scheduler ---")
            break

    print("--- exit main thread ---")
