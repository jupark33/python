# 머리 속으로 그림. 
# 테스트 안됨.


from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import time

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
        print("%s task id[%s] : %d" %(type, job_id, time.localtime().tm_sec))

    # 스케줄러생성, 월-금, 0시~23시, 2초 간격
    def scheduler(self, job_id):
        print("%s Scheduler Start" % type)
        self.sched.add_job(self.task, type, day_of_week='mon-fri', hour='0-23', second='*/2', id=job_id, args=(type, job_id))
 
if __name__ = '__main__':
    scheduler = Scheduler()
    scheduler.scheduler("1")
    
