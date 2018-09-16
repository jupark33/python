# http://www.engear.net/wp/python%EC%9C%BC%EB%A1%9C-windows-%EC%84%9C%EB%B9%84%EC%8A%A4-%EB%A7%8C%EB%93%A4%EA%B8%B0/

#Usage: 'svc_otm.py [options] install|update|remove|start [...]|stop|restart [...]|debug [...]'
#Options for 'install' and 'update' commands only:
# --username domain\username : The Username the service is to run under
# --password password : The password for the username
# --startup [manual|auto|disabled|delayed] : How the service starts, default = manual
# --interactive : Allow the service to interact with the desktop.
# --perfmonini file: .ini file to use for registering performance monitor data
# --perfmondll file: .dll file to use when querying the service for
#   performance data, default = perfmondata.dll
#Options for 'start' and 'stop' commands only:
# --wait seconds: Wait for the service to actually start or stop.
#                 If you specify --wait with the 'stop' option, the service
#                 and all dependent services will be stopped, each waiting
#                 the specified period.


import sys
# import os
import win32service
import win32serviceutil
import win32event
import servicemanager
import win32api
import traceback
import configparser
import logging
import os

class OtmService(win32serviceutil.ServiceFramework):

    _svc_name_ = "OtmSvc"
    _svc_display_name_ = "OtmService"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.haltEvent = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = False

        #pyinstaller를 사용하지 않는다면, elif 부분만 필요함
        if getattr(sys, 'frozen', False):
            #pyinstaller로 패키징한 실행파일의 경우
            self.cur_path = os.path.dirname(sys.executable)
        elif __file__:
            # *.py 형태의 파일로 실행할 경우 로직
            self.cur_path = os.path.dirname(os.path.abspath(__file__))

        # config = configparser.ConfigParser()
        # config.read(self.cur_path + "/opp.ini")
        #
        # str_log_level = config['GENERAL']['LOGLEVEL']
        # self._timeout = int(config['GENERAL']['CHECK_TERM'])
        # log_level = 0
        # if str_log_level == 'DEBUG':
        #     log_level = logging.DEBUG
        # elif str_log_level == 'ERROR':
        #     log_level = logging.ERROR
        # elif str_log_level == 'WARN':
        #     log_level = logging.WARN
        # else:
        #     log_level = logging.INFO
        #
        # logging.basicConfig(filename=self.cur_path + '/opp.log', format='%(asctime)s [%(levelname)-5s] %(message]s',
        #                     level=log_level)
        #
        # logging.info('SERVICE initialized.')
        # logging.info('LOG : ' + self.cur_path + "/opp.log")
        # logging.info("CHECK TERM : %d seconds" % (self._timeout / 1000))

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        win32event.SetEvent(self.haltEvent)

    def SvcDoRun(self):
        self.is_running = True
        logging.info("[SERVICE] Let's start.")

        while self.is_running:
            rc = win32event.WaitForSingleObject(self.haltEvent, self._timeout)

            if rc == win32event.WAIT_OBJECT_0:
                # Stop signal
                logging.info("[SERVICE] Stop Signal")
                break
            else:
                try:
                    logging.info("[SERVICE] RUN Check_otm function")
                    # 실제로 수행하는 메쏘드

                except:
                    logging.warning("[SERVICE] %s" % traceback.format_exc())

                logging.warning("[SERVICE] RETURN of check_otms function is : %s" % ret)

def ctrlHandler(strlType):
    return True

if __name__ == '__main__':

    #서비스로 동작하게 하기 위한 소스
    if getattr(sys, 'frozen', False):
        if len(sys.argv) == 1:
            #pyinstaller로 패키징하여, 서비스로 동작하게 하는 로직
            #아마도 StartServiceCtrlDispatcher부분에서 뭔가 Service 관리자와 통신하는게 있는듯하다.
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(OtmService)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            win32api.SetConsoleCtrlHandler(ctrlHandler, True)
            win32serviceutil.HandleCommandLine(OtmService)

    else:
        # .py 소스를 이용하여 서비스로 동작하게 하는 로직
        win32api.SetConsoleCtrlHandler(ctrlHandler, True)
        win32serviceutil.HandleCommandLine(OtmService)
