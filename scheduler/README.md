# 매분 2초 마다 스케줄러 실행
def scheduler(self, type, job_id): <br>
    print('scheduler, type : ' + type + ', job_id : ' + job_id) 
	self.sched.add_job(self.task, type, day_of_week='mon-sun', \
                 hour='0-23', minute='*/1', second='2', id=job_id, args=(type, job_id))
