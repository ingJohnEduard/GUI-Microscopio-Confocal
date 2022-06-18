
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class PyToggle(QCheckBox):
	def __init__(
		self,
		width = 60,
		bg_color = "#e5e9ff",
		circle_color = "#DDD",
		active_color = "#2222",
		animation_curve = QEasingCurve.OutBounce
	):

		QCheckBox.__init__(self)

		self.setFixedSize(width, 28)
		self.setCursor(Qt.PointingHandCursor)

		#Colors
		self._bg_color = bg_color
		self._circle_color = circle_color
		self._active_color = active_color

		#Create animation
		self._circle_position = 3
		self.animation = QPropertyAnimation(self, b"circle_position", self)
		self.animation.setEasingCurve(animation_curve)
		self.animation.setDuration(500)

		# connect checkbox
		self.stateChanged.connect(self.start_transition)

	def changeProperties(self,
		active_color = "#2222",):
		self._active_color = active_color

	# Create New Set And Get Propertie 
	@Property(float)
	def circle_position(self):
		return self._circle_position

	@circle_position.setter
	def circle_position(self, pos):
		self._circle_position = pos
		self.update()
	
	def start_transition(self, value):
		self.animation.stop() # stop animation if running
		if value:
			self.animation.setEndValue(self.width() - 26)
		else:
			self.animation.setEndValue(3)

		self.animation.start()

	#Set New Hit Area
	def hitButton(self, pos: QPoint):
		return self.contentsRect().contains(pos)

	#Draw new Items
	def paintEvent(self, e):
		#Set Painter
		p = QPainter(self)
		p.setRenderHint(QPainter.Antialiasing)

		#set as no pen
		p.setPen(Qt.NoPen)

		#draw rectangle
		rect = QRect(0,0,self.width(),self.height())

		if not self.isChecked():
			# Draw BG
			p.setBrush(QColor(self._bg_color))
			p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height()/2, self.height()/2)

			# Draw circle
			p.setBrush(QColor(self._circle_color))
			p.drawEllipse(self._circle_position,3,22,22)
		else:
			# Draw BG
			p.setBrush(QColor(self._active_color))
			p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height()/2, self.height()/2)

			# Draw circle
			p.setBrush(QColor(self._circle_color))
			p.drawEllipse(self._circle_position,3,22,22)

		#END DRAW
		p.end()
