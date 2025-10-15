import sys
from PyQt5.QtWidgets import (
	QApplication,
	QWidget,
)
from PyQt5 import QtCore
from PyQt5 import QtMultimedia
from PyQt5 import uic

#soundf = 'assets/sound/'
soundf = '/home/grv/Documents/py/lab3/assets/sound/'

class Piano(QWidget):
    def __init__(self):
        super().__init__()
		
        self.initUI()
		
    def initUI(self):
        uic.loadUi("piano.ui", self)

        self.player = QtMultimedia.QMediaPlayer()
        
        self.pbC.clicked.connect(self.playSound)
        self.pbD.clicked.connect(self.playSound)
        self.pbE.clicked.connect(self.playSound)
        self.pbF.clicked.connect(self.playSound)
        self.pbG.clicked.connect(self.playSound)
        self.pbA.clicked.connect(self.playSound)
        self.pbB.clicked.connect(self.playSound)

        self.pbMusic1.clicked.connect(self.playSound)
        self.pbStop.clicked.connect(self.player.stop)
        
    def playSound(self):
        media = QtCore.QUrl.fromLocalFile(soundf + self.sender().text() + '.wav')
        content = QtMultimedia.QMediaContent(media)
        self.player.setMedia(content)
        self.player.play()
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Piano()
    ex.show()
    sys.exit(app.exec())

