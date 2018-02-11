import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# kiwoom login
		self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
		self.kiwoom.dynamicCall("CommConnect()")

		# OpenAPI+ Event
		self.kiwoom.OnEventConnect.connect(self.event_connect)
		self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

		self.setWindowTitle("PyStock")
		self.setGeometry(300, 300, 300, 150)

		label = QLabel('종목코드: ', self)
		label.move(20, 20)

		self.code_edit = QLineEdit(self)
		self.code_edit.move(80, 20)
		self.code_edit.setText("039490")

		btn1 = QPushButton("조회", self)
		btn1.move(190, 20)
		btn1.clicked.connect(self.btn1_clicked)

		self.text_edit = QTextEdit(self)
		self.text_edit.setGeometry(10, 60, 280, 80)
		# self.text_edit.setEnabled(False)
		self.text_edit.setReadOnly(True)

		self.sb = self.text_edit.verticalScrollBar()
		self.sb.setValue(self.sb.maximum())

	def event_connect(self, err_code):
		if err_code == 0:
			self.text_edit.append("로그인 성공")

	def btn1_clicked(self):
		code = self.code_edit.text()
		#self.text_edit.append("종목코드: " + code)

		# SetInputValue
		self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "시장구분", "000")
		self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "정렬구분", "1")
		self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "시간구분", "2")
		self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "거래량구분", "5") #5천주 이상

		# CommRqData
		self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "거래량급등종목", "opt10023", 0, "0101")

	def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
		if rqname == "거래량급등종목":
			
			cnt = self.getRepeatCnt(trcode, rqname)
			self.text_edit.append("cnt : " + str(cnt))

			for i in range(cnt):
				res_code = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "종목코드")
				name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "종목명")
				volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, i, "현재거래량")

				self.text_edit.append("-- 번호 : " + str(i) + " ---")
				self.text_edit.append("종목코드:" + res_code.strip())
				self.text_edit.append("종목명:" + name.strip())			
				self.text_edit.append("현재거래량:" + volume.strip())

	def getRepeatCnt(self, trcode, rqname):
		count = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
		return count

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myWindow = MyWindow()
	myWindow.show()
	app.exec_()	
