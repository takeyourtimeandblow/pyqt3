import sys
import re
import statistics
import subprocess

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFileDialog
)
from PyQt5 import uic

class NumberCatcher(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
	    
    def initUI(self):
        uic.loadUi("number_catcher.ui", self)
        self.pbUpload.clicked.connect(self.upload)
        self.pbSave.clicked.connect(self.save)
        
    def upload(self):
        
        file_name = QFileDialog.getOpenFileName(
            self, 'Выбрать текст',
            './assets',
            'Текстовые файлы (*.txt);; Все файлы (*)')[0]
        
        if file_name:
            file_content = open(file_name).read()
            nums = [int(x) for x in re.sub(r' \D+-', '', file_content).split(' ')]
            
            self.lcdMax.display(str(max(nums)))
            self.lcdMin.display(str(min(nums)))
            self.lcdAvg.display(str(statistics.mean(nums)))
        
            self.pbSave.setEnabled(True)
    
    def save(self):
        try:
            path = f'/home/{subprocess.run("whoami", capture_output=True, text=True, check=True).stdout.strip()}/Documents'
        except subprocess.CalledProcessError as e:
            print("Failed to find username")
            
            path = './assets'
        finally:
            wr_file_name = QFileDialog.getSaveFileName(
                self,
                'Сохранить файл',
                path,
                'Текст с расширением .txt (*.txt);; Без расширения (*)')[0]
            if wr_file_name:
                wr_file = open(wr_file_name, 'w')
            
                txt = f'''Max: {self.lcdMax.value()}\nMin: {self.lcdMin.value()}\nAverage: {self.lcdAvg.value()}'''
                
                wr_file.write(txt)
                wr_file.close()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NumberCatcher()
    ex.show()
    sys.exit(app.exec())
