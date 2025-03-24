import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QTextEdit
)
from PyQt5.QtCore import Qt

class POSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("F1D022077-Muhammad Rifkyandryan Rustanto")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        self.products = {
            "Bimoli (Rp. 20,000)": 20000,
            "Beras 5 Kg (Rp. 75,000)": 75000,
            "Kecap ABC (Rp. 7,000)": 7000,
            "Saos Saset (Rp. 2,000)": 2000,
        }
        
        self.product_label = QLabel("Product")
        self.product_combo = QComboBox()
        self.product_combo.addItem("")  
        self.product_combo.addItems(self.products.keys())

        self.qty_label = QLabel("Quantity")
        self.qty_input = QLineEdit()
        self.qty_input.setPlaceholderText("Enter quantity")
        self.qty_input.setFixedWidth(182)

        self.discount_label = QLabel("Discount")
        self.discount_combo = QComboBox()
        self.discount_combo.addItems(["0%", "5%", "10%", "15%"])

        self.add_btn = QPushButton("Add to Cart")
        self.clear_btn = QPushButton("Clear")

        self.add_btn.clicked.connect(self.add_to_cart)
        self.clear_btn.clicked.connect(self.clear_fields)

        self.cart_display = QTextEdit()
        self.cart_display.setReadOnly(True)
        self.total_label = QLabel("Total: Rp. 0")

        product_layout = QHBoxLayout()
        product_layout.addWidget(self.product_label, alignment=Qt.AlignCenter)
        product_layout.addWidget(self.product_combo)

        qty_layout = QHBoxLayout()
        qty_layout.addWidget(self.qty_label, alignment=Qt.AlignCenter)
        qty_layout.addWidget(self.qty_input)

        discount_layout = QHBoxLayout()
        discount_layout.addWidget(self.discount_label, alignment=Qt.AlignCenter)
        discount_layout.addWidget(self.discount_combo)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.clear_btn)

        main_layout.addLayout(product_layout)
        main_layout.addLayout(qty_layout)
        main_layout.addLayout(discount_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.cart_display)
        main_layout.addWidget(self.total_label, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def add_to_cart(self):
        product = self.product_combo.currentText()
        quantity = self.qty_input.text()

        if not product:
            self.cart_display.append("Please select a product!")
            return
        if not quantity.isdigit() or int(quantity) <= 0:
            self.cart_display.append("Invalid quantity!")
            return

        quantity = int(quantity)
        price = self.products[product]
        discount = int(self.discount_combo.currentText().strip('%')) / 100
        total_price = quantity * price * (1 - discount)
        discount_text = f"(disc {int(discount * 100)}%)" if discount > 0 else ""

        self.cart_display.append(f"{product} - {quantity} x Rp. {total_price:,.0f} {discount_text}")
        self.update_total()

    def clear_fields(self):
        self.product_combo.setCurrentIndex(0)
        self.qty_input.clear()
        self.discount_combo.setCurrentIndex(0)
        self.cart_display.clear()
        self.total_label.setText("Total: Rp. 0")

    def update_total(self):
        total = 0
        for line in self.cart_display.toPlainText().split("\n"):
            if "Rp." in line:
                total += int(line.split("Rp. ")[-1].replace(",", "").split()[0])
        
        self.total_label.setText(f"Total: Rp. {total:,.0f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = POSApp()
    window.show()
    sys.exit(app.exec_())
