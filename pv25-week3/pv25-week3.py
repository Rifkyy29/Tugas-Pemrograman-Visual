import sys
import random
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QEvent

class MouseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Task Week 3 - (F1D022077 - Muhammad Rifkyandryan Rustanto)")
        self.setGeometry(100, 100, 500, 300)
        
        self.label = QLabel("x: 0, y: 0", self)
        self.label.adjustSize()
        self.setMouseTracking(True)

        self.label.setAttribute(Qt.WA_Hover, True)
        self.label.installEventFilter(self)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        self.label.setText(f"x: {x}, y: {y}")
        self.label.adjustSize()

    def eventFilter(self, obj, event):
        if obj == self.label and event.type() == QEvent.HoverEnter:
            self.moveLabel()
        return super().eventFilter(obj, event)

    def moveLabel(self):
        window_width = self.width()
        window_height = self.height()
        label_width = self.label.width()
        label_height = self.label.height()

        new_x = random.randint(0, window_width - label_width)
        new_y = random.randint(0, window_height - label_height)

        self.label.move(new_x, new_y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MouseTracker()
    ex.show()
    sys.exit(app.exec_())
