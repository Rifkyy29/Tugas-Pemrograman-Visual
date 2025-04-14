import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class FontAdjuster(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Font Size and Color Adjuster")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("F1D022077", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 30))
        self.label.setAutoFillBackground(True)

        self.font_slider = self.create_slider(20, 60, 30)
        self.font_slider.valueChanged.connect(self.update_font_size)

        self.bg_slider = self.create_slider(0, 255, 255)
        self.bg_slider.valueChanged.connect(self.update_colors)

        self.font_color_slider = self.create_slider(0, 255, 0)
        self.font_color_slider.valueChanged.connect(self.update_colors)

        
        layout.addWidget(self.label)
        layout.addLayout(self.labeled_slider("Font Size", self.font_slider))
        layout.addLayout(self.labeled_slider("Background Color", self.bg_slider))
        layout.addLayout(self.labeled_slider("Font Color", self.font_color_slider))
        

        self.setLayout(layout)
        self.update_colors() 

    def create_slider(self, min_val, max_val, default):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        return slider

    def labeled_slider(self, title, slider):
        h_layout = QHBoxLayout()
        label = QLabel(title)
        label.setFixedWidth(120)
        h_layout.addWidget(label)
        h_layout.addWidget(slider)
        return h_layout

    def update_font_size(self):
        size = self.font_slider.value()
        font = self.label.font()
        font.setPointSize(size)
        self.label.setFont(font)

    def update_colors(self):
        bg_gray = self.bg_slider.value()
        font_gray = self.font_color_slider.value()

        bg_color = QColor(bg_gray, bg_gray, bg_gray)
        font_color = QColor(font_gray, font_gray, font_gray)

        palette = self.label.palette()
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.WindowText, font_color)
        self.label.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FontAdjuster()
    window.resize(600, 300)
    window.show()
    sys.exit(app.exec_())
