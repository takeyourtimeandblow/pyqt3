import sys
from PyQt5.QtWidgets import (
	QApplication,
	QDialog,
	QMainWindow,
	QWidget,
	QTabWidget,
	QPlainTextEdit,
	QFileDialog,
	QAction
)
from PyQt5 import QtGui as qtg
from PyQt5 import uic
    
original_txts = []

file_names = []

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
		
        self.w = None
		
        self.initUI()
		
    def initUI(self):
        uic.loadUi("text_editor.ui", self)
	    
        original_txts.append('')
        file_names.append('')
	    
        self.tabWidget.setTabText(0, 'Новый')
        self.tabWidget.removeTab(1)
	    
        self.actOpen.triggered.connect(self.open)
        self.actNew.triggered.connect(self.newTab)
        self.actSave.triggered.connect(self.saveToFile)
	    
        self.tabWidget.findChild(QPlainTextEdit).textChanged.connect(self.toggleAsterisk)
        self.pbClose.clicked.connect(self.closeTab)
        self.tabWidget.currentChanged.connect(self.resizePlainText)

    def resizeEvent(self, event: qtg.QResizeEvent):
        new_size = event.size()
        old_size = event.oldSize()

        self.tabWidget.setFixedSize(new_size.width(), new_size.height())
        self.tabWidget.findChildren(QPlainTextEdit)[self.tabWidget.currentIndex()].setFixedSize(new_size.width(), new_size.height())

        super().resizeEvent(event)

    def open(self):
        try:
            file_names.append(QFileDialog.getOpenFileName(
	                self,
	                'Открыть файл',
	                './assets/',
	                'Без расширения или с (*)')[0])
            self.tabWidget.addTab(QPlainTextEdit(), file_names[-1][len(file_names[-1]) - file_names[-1][::-1].find('/'):])
            self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
            with open(file_names[-1], 'r') as file:
                original_txts.append(file.read())
            self.tabWidget.findChildren(QPlainTextEdit)[self.tabWidget.currentIndex()].textChanged.connect(self.toggleAsterisk)
            self.tabWidget.findChildren(QPlainTextEdit)[self.tabWidget.currentIndex()].setPlainText(original_txts[-1])
        except FileNotFoundError:
	        print('TextEditor.saveToFile() error: File was not found')
        
	
    def newTab(self):
	    self.tabWidget.addTab(QPlainTextEdit(), 'Новый')
	    original_txts.append('')
	    file_names.append('')
	    
	    self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
	    
	    self.tabWidget.findChildren(QPlainTextEdit)[self.tabWidget.currentIndex()].textChanged.connect(self.toggleAsterisk)
	    
    def saveToFile(self):
	    try:
	        index = self.tabWidget.currentIndex()

	        if not file_names[index]:
	            file_names[index] = QFileDialog.getSaveFileName(
	                self,
	                'Сохранить файл',
	                './assets/',
	                'Текст с расширением .txt (*.txt);; Без расширения (*)')[0]
	            
	            if not file_names[index]:
	                raise FileNotFoundError
	            
	            self.tabWidget.setTabText(
	                index,
	                file_names[index][len(file_names[index]) - file_names[index][::-1].find('/'):]
	            )
	            from PyQt5 import QtGui as qtg
	        with open(file_names[index], "w") as file:
	            file.write(self.tabWidget.findChildren(QPlainTextEdit)[index].toPlainText())
	        original_txts[index] = self.tabWidget.findChildren(QPlainTextEdit)[index].toPlainText()
	        
	    except FileNotFoundError:
	        print('TextEditor.saveToFile() error: File was not found')

    def closeTab(self):
        index = self.tabWidget.currentIndex()
        txt_check = self.tabWidget.findChildren(QPlainTextEdit)[index].toPlainText()
        if txt_check != original_txts[index]:
            self.dialogWindow(txt_check, index)
        self.tabWidget.findChildren(QPlainTextEdit).pop(self.tabWidget.currentIndex())
        self.tabWidget.removeTab(index)
        

	
    def toggleAsterisk(self):
	    index = self.tabWidget.currentIndex()
	    
	    if self.sender().toPlainText() == original_txts[index]:
	        self.tabWidget.setTabText(
	            index,
	            self.tabWidget.tabText(index).replace('*', '')
	        )
	    elif '*' not in self.tabWidget.tabText(index):
	        self.tabWidget.setTabText(
	            index,
	            self.tabWidget.tabText(index) + '*'
	        )
    
    def resizePlainText(self, index):
        self.tabWidget.findChildren(QPlainTextEdit)[index].setFixedSize(self.size().width(), self.size().height())

    def dialogWindow(self, txt, i):
	    if self.w is None:
	        self.w = TextEditDialog(txt, i)
	        self.w.show()
	    else:
	        self.w = None
	        self.closeTab()
	
class TextEditDialog(QDialog):
    def __init__(self, txt, i):
        super().__init__()
        
        self.txt = txt
        self.i = i
        self.c = False
        self.initUI()
    
    def initUI(self):
        uic.loadUi("text_editor_dialog.ui", self)
        self.buttonBox.buttons()[1].clicked.connect(self.closeNoChanges)
        self.buttonBox.buttons()[0].clicked.connect(self.save)

    def save(self):
        try:
            if not file_names[self.i]:
                file_names[self.i] = QFileDialog.getSaveFileName(
	                self,
	                'Сохранить файл',
	                './assets/',
	                'Текст с расширением .txt (*.txt);; Без расширения (*)')[0]
                if not file_names[self.i]:
                    raise FileNotFoundError
	                
                with open(file_names[self.i], 'w') as file:
                    file.write(self.txt)
                file_names.pop(self.i)
                original_txts.pop(self.i)
        except FileNotFoundError:
	        print('TextEditor.saveToFile() error: File was not found')

    def closeNoChanges(self):
        original_txts.pop(self.i)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextEditor()
    ex.show()
    sys.exit(app.exec())

