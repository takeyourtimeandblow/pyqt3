from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QFileDialog,
                            QGraphicsOpacityEffect)
from PyQt5.QtGui import QPainter, QPixmap, QPaintDevice
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys

class ImageAlpha(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pixmap = None

        self.painter = None

        self.opacity_effect = None

        self.initUI()

        self.open_image_dialog()

    def initUI(self):
        uic.loadUi('image_processor_alpha.ui', self)
        #uic.loadUi('image_processor.ui', self)

        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.changeAlpha)


    def changeAlpha(self, val):
        opacity = val / 100.0  # Convert slider value to a 0.0-1.0 range
        self.opacity_effect.setOpacity(opacity)
        
    def open_image_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            'Выберите изображение', 
            '', 
            'Images (*.png *.jpg *.jpeg *.bmp *.gif)'
        )
        
        if file_name:
            self.load_image(file_name)

    def load_image(self, file_path):
        self.pixmap = QPixmap(file_path)
        
        if self.pixmap.isNull():
            QMessageBox.warning(self, 'Ошибка', 'Не удалось загрузить изображение')
            return

        self.image_label.setPixmap(self.pixmap)
        self.opacity_effect = QGraphicsOpacityEffect(self.image_label)
        self.image_label.setGraphicsEffect(self.opacity_effect)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageAlpha()
    window.show()
    sys.exit(app.exec_())
