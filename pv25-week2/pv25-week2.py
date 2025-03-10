import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QRadioButton, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox
)

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Week 2 : Layout - User Registration Form")
        self.setGeometry(100, 100, 400, 350)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.identity_group = QGroupBox("Identitas")
        self.identity_layout = QVBoxLayout()
        self.name_label = QLabel("Nama : ")
        self.nim_label = QLabel("Nim : ")
        self.class_label = QLabel("Kelas : ")
        
        self.identity_layout.addWidget(self.name_label)
        self.identity_layout.addWidget(self.nim_label)
        self.identity_layout.addWidget(self.class_label)
        self.identity_group.setLayout(self.identity_layout)
        main_layout.addWidget(self.identity_group)

        nav_group = QGroupBox("Navigation")
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(QPushButton("Home"))
        nav_layout.addWidget(QPushButton("About"))
        nav_layout.addWidget(QPushButton("Contact"))
        nav_group.setLayout(nav_layout)
        main_layout.addWidget(nav_group)

        self.setStyleSheet("""
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid purple;
                outline: none;
            }
        """)

        form_group = QGroupBox("User Registration")
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.nim_input = QLineEdit()
        self.class_input = QLineEdit()

        form_layout.addRow("Full Name:", self.name_input)
        form_layout.addRow("NIM:", self.nim_input)
        form_layout.addRow("Class:", self.class_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)

        gender_layout = QHBoxLayout()
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        form_layout.addRow("Gender:", gender_layout)

        self.country_combo = QComboBox()
        self.country_combo.addItems(["Select", "Indonesia", "Australia", "USA", "UK" ])
        form_layout.addRow("Country:", self.country_combo)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)

        centered_form_layout = QVBoxLayout()
        centered_form_layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        form_group.setLayout(centered_form_layout)
        main_layout.addWidget(form_group)

        action_group = QGroupBox("Actions")
        action_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.cancel_button = QPushButton("Cancel")
        action_layout.addWidget(self.submit_button)
        action_layout.addWidget(self.cancel_button)
        action_group.setLayout(action_layout)
        main_layout.addWidget(action_group)

        self.submit_button.clicked.connect(self.submit_form)
        self.cancel_button.clicked.connect(self.clear_form)

        self.setLayout(main_layout)

    def submit_form(self):
        name = self.name_input.text()
        nim = self.nim_input.text()
        kelas = self.class_input.text()
        
        self.name_label.setText(f"Nama : {name}")
        self.nim_label.setText(f"Nim : {nim}")
        self.class_label.setText(f"Kelas : {kelas}")

        self.clear_registration_form()

    def clear_form(self):
        self.clear_registration_form()
        self.name_label.setText("Nama : ")
        self.nim_label.setText("Nim : ")
        self.class_label.setText("Kelas : ")

    def clear_registration_form(self):
        self.name_input.clear()
        self.nim_input.clear()
        self.class_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.male_radio.setChecked(False)
        self.female_radio.setChecked(False)
        self.country_combo.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec_())
