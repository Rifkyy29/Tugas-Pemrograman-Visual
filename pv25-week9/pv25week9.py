import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QInputDialog, QGridLayout, QLineEdit
)

class InputDialogDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Dialog demo F1D022077_Muhammad Rifkyandryan Rustanto")
        self.setGeometry(100, 100, 400, 200)

        layout = QGridLayout()

        self.btn_list = QPushButton("Choose from list")
        self.btn_list.clicked.connect(self.show_list_dialog)
        self.label_list = QLineEdit()

        self.btn_name = QPushButton("Get name")
        self.btn_name.clicked.connect(self.show_name_dialog)
        self.label_name = QLineEdit()

        self.btn_integer = QPushButton("Enter an integer")
        self.btn_integer.clicked.connect(self.show_integer_dialog)
        self.label_integer = QLineEdit()
        
        layout.addWidget(self.btn_list, 0, 0)
        layout.addWidget(self.label_list, 0, 1)
        layout.addWidget(self.btn_name, 1, 0)
        layout.addWidget(self.label_name, 1, 1)
        layout.addWidget(self.btn_integer, 2, 0)
        layout.addWidget(self.label_integer, 2, 1)

        self.setLayout(layout)

    def show_list_dialog(self):
        items = ("C", "Java", "Python")
        item, ok = QInputDialog.getItem(self, "Select Input Dialog", "List of languages:", items, 0, False)
        if ok and item:
            self.label_list.setText(item)

    def show_name_dialog(self):
        text, ok = QInputDialog.getText(self, "Text Input Dialog", "Enter your name:")
        if ok and text:
            self.label_name.setText(text)

    def show_integer_dialog(self):
        number, ok = QInputDialog.getInt(self, "Integer Input Dialog", "Enter a number:")
        if ok:
            self.label_integer.setText(str(number))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = InputDialogDemo()
    demo.show()
    sys.exit(app.exec_())
