from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QTimeEdit, QListWidgetItem, QMessageBox, QScrollArea
from PyQt5.QtCore import Qt, QDate, QTime
import sys
import os

class ToDoListApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'todolist.ui'), self)

        self.tasks = []

        self.add_task_btn.clicked.connect(self.add_task)

        self.scroll_areas = {
            "all": self.scrollAreaSemua,
            "open": self.scrollAreaBelum,
            "closed": self.scrollAreaSudah
        }

        self.task_layouts = {}
        for key, scroll_area in self.scroll_areas.items():
            content_widget = QWidget()
            layout = QVBoxLayout(content_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)
            scroll_area.setWidget(content_widget)
            scroll_area.setWidgetResizable(True)
            self.task_layouts[key] = layout

        self.refresh_task_list()

    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            task = {
                "date": self.calendar.selectedDate(),
                "time": self.time_edit.time(),
                "text": task_text,
                "priority": self.priority_combo.currentText(),
                "completed": False
            }
            self.tasks.append(task)
            self.task_input.clear()
            self.refresh_task_list()

    def refresh_task_list(self):
        for layout in self.task_layouts.values():
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        if not self.tasks:
            return

        self.tasks.sort(key=lambda t: (
            t["date"],
            t["time"],
            0 if t["priority"] == "Prioritas" else 1
        ))

        for key, layout in self.task_layouts.items():
            filter_fn = lambda t: True if key == "all" else (not t["completed"] if key == "open" else t["completed"])
            current_date = None
            for task in filter(filter_fn, self.tasks):
                if task["date"] != current_date:
                    current_date = task["date"]
                    label = QLabel(current_date.toString("dd MMMM yyyy"))
                    label.setStyleSheet("font-size: 14px; font-weight: bold;") 
                    layout.addWidget(label)

                task_widget = QWidget()
                task_layout = QVBoxLayout(task_widget)

                status = "[SELESAI]" if task["completed"] else "[BELUM]"
                title = f"{task['time'].toString('HH:mm')} {status}"
                label = QLabel(title)
                label.setStyleSheet("font-size: 12px; font-weight: bold;")  

                task_label = QLabel(task["text"])
                task_label.setStyleSheet("font-size: 12px;")  

                if task["priority"] == "Prioritas":
                    task_label.setText("⭐ " + task_label.text())

                if task["completed"]:
                    task_widget.setStyleSheet("background-color: lightgreen; border-radius: 10px;")
                else:
                    task_widget.setStyleSheet("background-color: lightcoral; border-radius: 10px;")

                button_layout = QHBoxLayout()
                done_btn = QPushButton("Selesai" if not task["completed"] else "Batalkan")
                edit_btn = QPushButton("Edit")
                delete_btn = QPushButton("Hapus")

                done_btn.clicked.connect(lambda checked, t=task: self.toggle_task(t))
                edit_btn.clicked.connect(lambda checked, t=task: self.edit_task(t))
                delete_btn.clicked.connect(lambda checked, t=task: self.delete_task(t))

                button_layout.addWidget(done_btn)
                button_layout.addWidget(edit_btn)
                button_layout.addWidget(delete_btn)

                task_layout.addWidget(label)
                task_layout.addWidget(task_label)
                task_layout.addLayout(button_layout)
                
                task_widget.setFixedHeight(75)  

                layout.addWidget(task_widget)

    def toggle_task(self, task):
        task["completed"] = not task["completed"]
        self.refresh_task_list()

    def edit_task(self, task):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Edit Aktivitas")
        
        layout = QtWidgets.QFormLayout(dialog)

        # Edit Task Text
        task_text_input = QtWidgets.QLineEdit(dialog)
        task_text_input.setText(task["text"])
        layout.addRow("Aktivitas:", task_text_input)

        # Edit Time
        time_picker = QtWidgets.QTimeEdit(dialog)
        time_picker.setTime(task["time"])
        time_picker.setDisplayFormat("HH:mm")  
        layout.addRow("Jam:", time_picker)

        # Edit Priority
        priority_combo = QtWidgets.QComboBox(dialog)
        priority_combo.addItems(["Biasa", "Prioritas"])
        priority_combo.setCurrentIndex(0 if task["priority"] == "Biasa" else 1)
        layout.addRow("Prioritas:", priority_combo)

        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, dialog)
        layout.addWidget(buttons)
        
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            task["text"] = task_text_input.text().strip()
            task["time"] = time_picker.time()
            task["priority"] = priority_combo.currentText()

            self.refresh_task_list() 



    def delete_task(self, task):
        confirm = QMessageBox.question(self, "Konfirmasi", "Yakin ingin menghapus aktivitas ini?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.tasks.remove(task)
            self.refresh_task_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoListApp()
    window.show()
    sys.exit(app.exec_())
