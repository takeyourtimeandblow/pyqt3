import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QPushButton, QComboBox, QFileDialog,
    QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage, QTransform
from PyQt5.QtCore import Qt
from PyQt5 import uic

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.original_image = None
        self.current_image = None
        self.rotation = 0
        self.channel = 'RGB'
        
        # Автоматически открываем диалог выбора изображения при старте
        self.open_image_dialog()

    def initUI(self):
        uic.loadUi('image_processor.ui', self)

        self.channel_combo.currentTextChanged.connect(self.apply_channel)
        self.rotate_left_btn.clicked.connect(self.rotate_left)
        self.rotate_right_btn.clicked.connect(self.rotate_right)
        self.load_btn.clicked.connect(self.open_image_dialog)

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
        pixmap = QPixmap(file_path)
        
        if pixmap.isNull():
            QMessageBox.warning(self, 'Ошибка', 'Не удалось загрузить изображение')
            return

        # Проверяем, является ли изображение квадратным
        if pixmap.width() != pixmap.height():
            # Обрезаем до квадрата по минимальной стороне
            size = min(pixmap.width(), pixmap.height())
            pixmap = pixmap.copy(0, 0, size, size)
            QMessageBox.information(self, 'Информация', 
                                  'Изображение было обрезано до квадратной формы')

        self.original_image = pixmap.toImage()
        self.current_image = self.original_image.copy()
        self.rotation = 0
        self.channel = 'RGB'
        self.channel_combo.setCurrentIndex(0)
        self.update_display()

    def apply_channel(self, channel_text):
        if self.original_image is None:
            return
        
        self.channel = channel_text
        self.update_display()

    def rotate_left(self):
        self.rotation = (self.rotation - 90) % 360
        self.update_display()

    def rotate_right(self):
        self.rotation = (self.rotation + 90) % 360
        self.update_display()

    def update_display(self):
        if self.original_image is None:
            return

        # Создаем копию оригинального изображения
        image = self.original_image.copy()

        # Применяем цветовой канал
        if self.channel != 'RGB':
            image = self.apply_color_channel(image, self.channel)

        # Применяем поворот
        if self.rotation != 0:
            transform = image.transformed(
                image.trueMatrix(
                    QTransform().rotate(self.rotation), 
                    image.width(), 
                    image.height()
                )
            )
            image = transform

        # Обновляем отображение
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.width() - 10, 
                self.image_label.height() - 10,
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
        )

    def apply_color_channel(self, image, channel):
        """Оставляет только выбранный цветовой канал"""
        for y in range(image.height()):
            for x in range(image.width()):
                color = image.pixelColor(x, y)
                match channel:
                    case 'R':
                        new_color = (color.red(), 0, 0)
                    case 'G':
                        new_color = (0, color.green(), 0)                    
                    case 'B':
                        new_color = (0, 0, color.blue())                
                    case _:
                        new_color = (color.red(), color.green(), color.blue())
                
                image.setPixelColor(x, y, 
                    type(color)(*new_color, color.alpha()))

        return image

def main():
    app = QApplication(sys.argv)
    processor = ImageProcessor()
    processor.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

