import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QSlider, QLabel, QPushButton, QFileDialog, 
                             QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor

class LSystemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle_step = 60
        self.axiom = ""
        self.rules = {}
        self.current_string = ""
        self.current_iteration = 0
        self.setMinimumSize(1200, 600)
        
    def set_system(self, angle_step, axiom, rules):
        self.angle_step = angle_step
        self.axiom = axiom
        self.rules = rules
        self.current_iteration = 0
        self.current_string = axiom
        self.update()
    
    def set_iteration(self, iteration):
        self.current_iteration = iteration
        self.current_string = self.axiom
        for _ in range(iteration):
            new_string = ""
            for char in self.current_string:
                if char in self.rules:
                    new_string += self.rules[char]
                else:
                    new_string += char
            self.current_string = new_string
        self.update()
    
    def paintEvent(self, event):
        if not self.current_string:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(255, 255, 255))
        
        # Начальные параметры
        x = 20
        y = self.height() - 20
        angle = 0
        step = min(self.width(), self.height()) / 100
        stack = []
        
        pen = QPen(QColor(0, 100, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        
        # Обработка символов L-системы
        for char in self.current_string:
            if char == 'F':
                # Движение вперед с рисованием
                new_x = x + step * math.cos(math.radians(angle))
                new_y = y + step * math.sin(math.radians(angle))
                painter.drawLine(int(x), int(y), int(new_x), int(new_y))
                x, y = new_x, new_y
            elif char == 'f':
                # Движение вперед без рисования
                x += step * math.cos(math.radians(angle))
                y += step * math.sin(math.radians(angle))
            elif char == '+':
                # Поворот налево
                angle += self.angle_step
            elif char == '-':
                # Поворот направо
                angle -= self.angle_step
            elif char == '[':
                # Сохраняем текущее состояние
                stack.append((x, y, angle))
            elif char == ']':
                # Восстанавливаем состояние
                if stack:
                    x, y, angle = stack.pop()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("L-System Viewer")
        self.setGeometry(100, 100, 1200, 600)
        
        # Центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Панель управления
        control_layout = QHBoxLayout()
        
        self.open_button = QPushButton("Открыть файл")
        self.open_button.clicked.connect(self.open_file)
        control_layout.addWidget(self.open_button)
        
        self.file_label = QLabel("Файл не выбран")
        control_layout.addWidget(self.file_label)
        
        control_layout.addStretch(Qt.Horizontal)
        
        self.iteration_label = QLabel("Шаг: 0")
        control_layout.addWidget(self.iteration_label)
        
        layout.addLayout(control_layout)
        
        # Слайдер
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(5)
        self.slider.valueChanged.connect(self.slider_changed)
        layout.addWidget(self.slider)
        
        # Виджет для отображения L-системы
        self.lsystem_widget = LSystemWidget()
        layout.addWidget(self.lsystem_widget)
        
        # Переменные для хранения данных системы
        self.system_name = ""
        self.angle_divisor = 6
        self.axiom = ""
        self.rules = {}
    
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл L-системы", "", "Text files (*.txt)")
        
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    lines = [line.strip() for line in file.readlines() if line.strip()]
                
                if len(lines) < 3:
                    QMessageBox.warning(self, "Ошибка", "Файл должен содержать как минимум 3 строки")
                    return
                
                # Парсинг файла
                self.system_name = lines[0]
                self.angle_divisor = int(lines[1])
                self.axiom = lines[2]
                self.rules = {}
                
                for line in lines[3:]:
                    if ' ' in line:
                        key, value = line.split(' ', 1)
                        self.rules[key] = value
                
                # Настройка интерфейса
                self.setWindowTitle(f"L-System Viewer - {self.system_name}")
                self.file_label.setText(f"Файл: {file_name.split('/')[-1]}")
                
                angle_step = 360 / self.angle_divisor
                self.lsystem_widget.set_system(angle_step, self.axiom, self.rules)
                self.slider.setValue(0)
                
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def slider_changed(self, value):
        self.iteration_label.setText(f"Шаг: {value}")
        self.lsystem_widget.set_iteration(value)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
