import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QFormLayout, QMessageBox, QShortcut
)
from PyQt5.QtGui import QKeySequence

class FormValidationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form Validation-F1D022077_Muhammad Rifkyandryan Rustanto")
        self.setGeometry(200, 200, 400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.age_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.phone_input.setInputMask("+62 000 0000 0000")
        self.address_input = QTextEdit()
        self.gender_input = QComboBox()
        self.gender_input.addItems(["", "Male", "Female", "Other"])
        self.education_input = QComboBox()
        self.education_input.addItems(["", "High School", "Diploma", "Bachelor", "Master", "PhD"])

        self.save_btn = QPushButton("Save")
        self.clear_btn = QPushButton("Clear")

        layout.addRow("Name:", self.name_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Age:", self.age_input)
        layout.addRow("Phone Number:", self.phone_input)
        layout.addRow("Address:", self.address_input)
        layout.addRow("Gender:", self.gender_input)
        layout.addRow("Education:", self.education_input)
        layout.addRow(self.save_btn, self.clear_btn)

        self.save_btn.clicked.connect(self.validate_form)
        self.clear_btn.clicked.connect(self.clear_form)

        QShortcut(QKeySequence("Q"), self, activated=self.close)

        self.setLayout(layout)

    def validate_form(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        age = self.age_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.toPlainText().strip()
        gender = self.gender_input.currentText()
        education = self.education_input.currentText()

        if not all([name, email, age, phone, address]) or \
        gender == "" or education == "":
            self.show_message("All field are required.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.show_message("Please enter a valid email address.")
            return
        if not age.isdigit():
            self.show_message("Please enter a valid age (integer value).")
            return
        if not re.match(r"\+62 \d{3} \d{4} \d{4}", phone):
            self.show_message("Please enter a valid 13 digit phone number.")
            return

        address_parts = [part.strip() for part in address.split(',')]
        if len(address_parts) != 4 or not all(address_parts):
            self.show_message("Address must follow format: desa, kecamatan, kabupaten, provinsi.")
            return
            
        self.show_message("Profile saved successfully.", QMessageBox.Information)
        self.clear_form()


    def clear_form(self):
        self.name_input.clear()
        self.email_input.clear()
        self.age_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.education_input.setCurrentIndex(0)

    def show_message(self, message, icon=QMessageBox.Warning):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(" ")
        msg.setText(message)
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = FormValidationApp()
    form.show()
    sys.exit(app.exec_())
