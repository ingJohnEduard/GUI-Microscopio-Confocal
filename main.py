import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
#Import UIS
from main_window import Ui_MainWindow

#Import splash_screen display
from splash_screen import Ui_SplashScreen
from progress_bar import CircularProgress
from program import SetupArduino, CamUsb, Escaneo, cv2, plt


class SplashScreen(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = Ui_SplashScreen()
		self.ui.setupUi(self)

		self.setWindowFlag(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.counter = 0
		self.progress = CircularProgress()
		self.progress.width = 260
		self.progress.height = 260
		self.progress.value = 0
		self.progress.setFixedSize(self.progress.width ,self.progress.height)
		self.progress.move(18,18)
		self.progress.add_shadow(True)
		self.progress.bg_color = QColor(68, 71, 90, 140)
		self.progress.font_size = 40
		self.progress.progress_width = 15
		self.progress.setParent(self.ui.centralwidget)
		self.progress.show()

		self.Shadow = QGraphicsDropShadowEffect(self)
		self.Shadow.setBlurRadius(15)
		self.Shadow.setXOffset(0)
		self.Shadow.setYOffset(0)
		self.Shadow.setColor(QColor(0,0,0,100))
		self.setGraphicsEffect(self.Shadow)

		#QTIMER
		self.timer = QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(20)


		self.show()

	def update(self):

		self.progress.set_value(self.counter)

		if self.counter >= 100:
			self.timer.stop()
			self.main = MainWindow()
			self.main.show()

			self.close()

		self.counter += 1



class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.counter = 0
		self.progressMain = CircularProgress()
		self.progressMain.width = 100
		self.progressMain.height = 100
		self.progressMain.value = 0
		self.progressMain.setFixedSize(self.progressMain.width ,self.progressMain.height)
		self.progressMain.move(250+220/2-self.progressMain.width+70,10+350-self.progressMain.height)
		self.progressMain.add_shadow(True)
		self.progressMain.progress_color = 0xff79c6
		self.progressMain.text_color = 0xff79c6
		self.progressMain.font_size = 20
		self.progressMain.progress_width = 8
		self.progressMain.setParent(self.ui.centralwidget)
		self.progressMain.show()

		self.Shadow = QGraphicsDropShadowEffect(self)
		self.Shadow.setBlurRadius(10)
		self.Shadow.setXOffset(0)
		self.Shadow.setYOffset(0)
		self.Shadow.setColor(QColor(0,0,0,100))
		self.setGraphicsEffect(self.Shadow)
	

		self.show()
		self.ui.toggle.stateChanged.connect(self.toggle_state)
		self.ui.pushButton.clicked.connect(self.start_scan)
		self.ui.preview_cam.clicked.connect(self.start_preview)
		self.ui.tomar_foto.clicked.connect(self.take_picture)
		self.ui.change_ROI.clicked.connect(self.take_ROI)
		# create thread
		self.thread_toggle = QThread()
		# create object which will be moved to another thread
		self.setupArduino = SetupArduino()
		# move object to another thread
		self.setupArduino.moveToThread(self.thread_toggle)
        # connect signals from this object to slot in GUI thread
		self.setupArduino.signalOpen.connect(self.open_arduino)
		self.setupArduino.signalClose.connect(self.close_arduino)

		self.thread_toggle.start()

		#self.setupArduino.signalClose.connect(self.close_arduino)

	@Slot(int, int)
	def update2(self, total, value):
		#total = self.escaneo.pixelesY
		#value = self.escaneo.j
		self.counter = int(value*100/total)
		self.progressMain.set_value(self.counter)

	#def change_text(self):
	#	self.ui.Conexion.setText("Pelao")
	#	print("Pelao")

	def take_text(self):
		a = self.ui.Edit_Alto.text()
		b = self.ui.Edit_Ancho.text()
		c = self.ui.Resolucion_Edit.text()
		print(a)
		return int(a), int(b), float(c)

	def take_ROI(self):
		X1 = self.ui.Edit_x1.text()
		Y1 = self.ui.Edit_y1.text()
		X2 = self.ui.Edit_x2.text()
		Y2 = self.ui.Edit_y2.text()
		file = open ('ROI.txt','w')
		file.write(X1)
		file.write("\n")
		file.write(Y1)
		file.write("\n")
		file.write(X2)
		file.write("\n")
		file.write(Y2)
		file.close()
		print(X1)

	def toggle_state(self):
		if self.ui.toggle.isChecked():
			QTimer.singleShot(0, self.setupArduino.init_arduino)
		else:
			self.setupArduino.close_arduino(self.arduino)

	def start_scan(self):
		if self.ui.pushButton.isChecked():
			[limiteX, limiteY, resolucion] = self.take_text()
			self.thread_escaneo = QThread()
			self.thread_escaneo.setTerminationEnabled(enabled=True)
			self.escaneo = Escaneo(limiteX, limiteY, resolucion, self.arduino)
			self.escaneo.moveToThread(self.thread_escaneo)
			self.escaneo.signalFrame.connect(self.show_frame)
			self.escaneo.SignalBar.connect(self.update2)
			self.thread_escaneo.started.connect(self.escaneo.RunScan)
			self.thread_escaneo.start()
		else:
			print("finish loop")
			self.escaneo.end(False)
			self.escaneo.cam.release()
			self.thread_escaneo.quit()

	def start_preview(self):
		if self.ui.preview_cam.isChecked():
			self.thread_preview = QThread()
			self.thread_preview.setTerminationEnabled(enabled=True)
			self.preview = CamUsb()
			self.preview.moveToThread(self.thread_preview)
			self.preview.SignalPreview.connect(self.show_frame)
			#self.preview.SignalBar.connect(self.update2)
			self.thread_preview.started.connect(self.preview.RunPreview)
			self.thread_preview.start()
		else:
			print("finish preview")
			self.preview.EndPreview(False)
			self.thread_preview.quit()

	def take_picture(self):
		cam = CamUsb()
		ret,frame = cam.preview_cam.read()
		ret,frame = cam.preview_cam.read()
		plt.imshow(frame)
		plt.show()



	@Slot(object)
	def show_frame(self, frame):
		cv2.imshow('Visor', frame)

	@Slot(str, object)
	def open_arduino(self, string, arduino):
		self.arduino = arduino
		print(string)

	@Slot(str)
	def close_arduino(self, string):
		print(string)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec())