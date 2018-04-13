import urllib3
from util.StringUtil import change_hour_minute, print_log, timestamp_to_time
from util.slackUtil import postMsg, web_hook_sendMsg
from bs4 import BeautifulSoup
from xml.dom import minidom
from datetime import datetime, timedelta
import time
import datetime
import requests
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json

class Kb_Status(object):
	def __init__(self):
		cnt = 0
		volume_up = 0
		volume_down = 0
		list_volume = list()
	
	def chk_vol(self):
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		url = 'https://api.korbit.co.kr/v1/ticker/detailed'
		http = urllib3.PoolManager()
		r = http.request('GET', url)
		r_json = json.loads(r.data.decode('utf-8'))
		r_json_size = len(r_json)
		#print(str(r_json_size))
		
		ts = r_json['timestamp']
		time_status = timestamp_to_time(ts)
		volume = r_json['volume']
		str_now = getNow()
		
		#print("[%s] %s task id[%s] time[%s] volume[%s]" % (str_now, type, job_id, time_status, volume))
		#list set data
		len_list_volume = len(list_volume)
		if (len_list_volume < 10):
			# volume을 실수로 변경
			# list에 volume 저장
			
			list_volume[len_list_volume] = float(volume)
		else:
			# up, down, even 체크
			# noti
			# list 전체 삭제
			
