import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QSlider, QColorDialog, QLabel)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5 import uic

class SmileyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.smiley_color = QColor(255, 255, 0)  # Желтый по умолчанию
        self.scale_factor = 1.0  # Начальный масштаб
        self.setMinimumSize(400, 400)

    def set_smiley_color(self, color):
        self.smiley_color = color
        self.update()  # Перерисовываем виджет

    def set_scale_factor(self, factor):
        self.scale_factor = factor / 50.0  # Преобразуем значение слайдера (0-100) в масштаб (0.0-2.0)
        self.update()  # Перерисовываем виджет

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Определяем базовые размеры с учетом масштаба
        base_size = min(self.width(), self.height()) * 0.8 * self.scale_factor
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Рисуем голову (желтый круг)
        painter.setBrush(QBrush(self.smiley_color))
        painter.setPen(QPen(Qt.black, 2))
        head_radius = base_size / 2
        painter.drawEllipse(int(center_x - head_radius), int(center_y - head_radius), 
                           int(base_size), int(base_size))
        
        # Рисуем глаза
        eye_radius = base_size * 0.1
        eye_offset_x = base_size * 0.2
        eye_offset_y = base_size * 0.2
        
        painter.setBrush(QBrush(Qt.black))
        # Левый глаз
        painter.drawEllipse(int(center_x - eye_offset_x - eye_radius), 
                           int(center_y - eye_offset_y - eye_radius), 
                           int(eye_radius * 2), int(eye_radius * 2))
        # Правый глаз
        painter.drawEllipse(int(center_x + eye_offset_x - eye_radius), 
                           int(center_y - eye_offset_y - eye_radius), 
                           int(eye_radius * 2), int(eye_radius * 2))
        
        # Рисуем улыбку (дуга)
        smile_rect_size = base_size * 0.6
        smile_rect_x = center_x - smile_rect_size / 2
        smile_rect_y = center_y - smile_rect_size / 3
        painter.setPen(QPen(Qt.black, 3))
        painter.drawArc(int(smile_rect_x), int(smile_rect_y), 
                       int(smile_rect_size), int(smile_rect_size), 
                       0, -180 * 16)  # 180 градусов в обратном направлении

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("smile.ui", self)      
        
        # Создаем виджет для рисования смайлика
        self.smiley_widget = SmileyWidget()
        self.layout.addWidget(self.smiley_widget)
        
        # Кнопка для выбора цвета
        self.color_button.clicked.connect(self.open_color_dialog)
        
        # Слайдер для масштаба
        self.scale_slider.setMinimum(10)  # 0.2 масштаб
        self.scale_slider.setMaximum(100)  # 2.0 масштаб
        self.scale_slider.setValue(50)     # 1.0 масштаб по умолчанию
        self.scale_slider.valueChanged.connect(self.slider_changed)

    @pyqtSlot()
    def open_color_dialog(self):
        # Открываем диалог выбора цвета :cite[3]:cite[8]
        color = QColorDialog.getColor()
        if color.isValid():
            self.smiley_widget.set_smiley_color(color)

    @pyqtSlot(int)
    def slider_changed(self, value):
        self.smiley_widget.set_scale_factor(value)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
