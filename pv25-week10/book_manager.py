import sys
import sqlite3
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox,
    QHeaderView, QMenuBar, QMenu, QAction, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class BookManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manajemen Buku")
        self.resize(800, 600)
        
        # Set window style
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: 'SF Pro Display', 'Segoe UI', Arial, sans-serif;
            }
            
            QLineEdit {
                padding: 8px 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            
            QLineEdit:focus {
                border-color: #007AFF;
                outline: none;
            }
            
            QPushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                background-color: #007AFF;
                color: white;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background-color: #0056CC;
            }
            
            QPushButton:pressed {
                background-color: #004BB5;
            }
            
            QPushButton#deleteButton {
                background-color: #FF6B6B;
            }
            
            QPushButton#deleteButton:hover {
                background-color: #FF5252;
            }
            
            QPushButton#exportButton {
                background-color: #51CF66;
            }
            
            QPushButton#exportButton:hover {
                background-color: #40C057;
            }
            
            QTableWidget {
                gridline-color: #ddd;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #E3F2FD;
                font-size: 14px;
            }
            
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f0f0f0;
                min-height: 20px;
                font-size: 14px;
            }
            
            QTableWidget QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #007AFF;
                background-color: white;
                color: #333;
                min-height: 30px;
                font-weight: normal;
            }
            
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 15px 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: 600;
                color: #495057;
                font-size: 14px;
                min-height: 25px;
            }
            
            QLabel {
                color: #333;
                font-size: 14px;
            }
            
            QMenuBar {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                padding: 4px;
            }
            
            QMenuBar::item {
                padding: 6px 12px;
                border-radius: 4px;
            }
            
            QMenuBar::item:selected {
                background-color: #007AFF;
                color: white;
            }
            
            QMenu {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 4px;
            }
            
            QMenu::item {
                padding: 8px 16px;
                border-radius: 4px;
            }
            
            QMenu::item:selected {
                background-color: #f0f0f0;
            }
        """)

        self.conn = sqlite3.connect("books.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.init_ui()
        self.load_data()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Menu bar
        self.create_menu_bar()
        main_layout.addWidget(self.menu_bar)
        
        # Content area
        content_widget = QWidget()
        content_widget.setContentsMargins(20, 20, 20, 20)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Manajemen Buku")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin: 10px 0;
            }
        """)
        content_layout.addWidget(title_label)
        
        # Form section
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        
        # Form inputs - compact horizontal layout
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        # Judul
        input_layout.addWidget(QLabel("Judul:"))
        self.title_input = QLineEdit()
        self.title_input.setMaximumWidth(150)
        input_layout.addWidget(self.title_input)
        
        # Pengarang
        input_layout.addWidget(QLabel("Pengarang:"))
        self.author_input = QLineEdit()
        self.author_input.setMaximumWidth(150)
        input_layout.addWidget(self.author_input)
        
        # Tahun
        input_layout.addWidget(QLabel("Tahun:"))
        self.year_input = QLineEdit()
        self.year_input.setMaximumWidth(80)
        input_layout.addWidget(self.year_input)
        
        # Save button
        self.save_button = QPushButton("Simpan")
        self.save_button.setMaximumWidth(80)
        self.save_button.clicked.connect(self.save_data)
        input_layout.addWidget(self.save_button)
        
        # Add stretch to push everything to the left
        input_layout.addStretch()
        
        form_layout.addLayout(input_layout)
        content_layout.addWidget(form_frame)
        
        # Search section
        search_layout = QHBoxLayout()
        search_label = QLabel("Cari Judul:")
        search_label.setMinimumWidth(80)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari judul...")
        self.search_input.textChanged.connect(self.search_data)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        content_layout.addLayout(search_layout)
        
        # Table section
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Pengarang", "Tahun"])
        self.table.cellChanged.connect(self.update_data)
        self.table.setEditTriggers(QTableWidget.DoubleClicked)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        
        # Set minimum table height
        self.table.setMinimumHeight(300)
        
        # Set row height
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.verticalHeader().setVisible(False)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.resizeSection(0, 60)  # ID column
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Judul
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Pengarang  
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.resizeSection(3, 80)  # Tahun column
        
        table_layout.addWidget(self.table)
        content_layout.addWidget(table_frame)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.delete_button = QPushButton("Hapus Data")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_data)
        btn_layout.addWidget(self.delete_button)
        
        self.export_button = QPushButton("Ekspor CSV")
        self.export_button.setObjectName("exportButton")
        self.export_button.clicked.connect(self.export_data)
        btn_layout.addWidget(self.export_button)
        
        content_layout.addLayout(btn_layout)
        
        # Footer
        footer_label = QLabel("Nama: Muhammad Rifkyandryan Rustanto | NIM: F1D022077")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                margin-top: 20px;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 6px;
            }
        """)
        content_layout.addWidget(footer_label)
        
        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)

    def create_menu_bar(self):
        self.menu_bar = QMenuBar(self)
        
        # File menu
        file_menu = self.menu_bar.addMenu("File")
        
        save_action = QAction("Simpan", self)
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)
        
        export_action = QAction("Ekspor ke CSV", self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Keluar", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = self.menu_bar.addMenu("Edit")
        
        delete_action = QAction("Hapus Data", self)
        delete_action.triggered.connect(self.delete_data)
        edit_menu.addAction(delete_action)
        
        # Data menu dengan submenu
        data_menu = self.menu_bar.addMenu("Data Buku")
        
        add_action = QAction("Data Buku", self)
        data_menu.addAction(add_action)
        
        export_submenu = data_menu.addMenu("Ekspor")
        
        csv_action = QAction("CSV", self)
        csv_action.triggered.connect(self.export_data)
        export_submenu.addAction(csv_action)

    def save_data(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        year = self.year_input.text().strip()
        
        if not title or not author or not year:
            QMessageBox.warning(self, "Peringatan", "Mohon isi semua field.")
            return
            
        if not year.isdigit():
            QMessageBox.warning(self, "Peringatan", "Tahun harus berupa angka.")
            return
            
        try:
            self.cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
                                (title, author, int(year)))
            self.conn.commit()
            
            # Clear inputs
            self.title_input.clear()
            self.author_input.clear()
            self.year_input.clear()
            
            self.load_data()
            QMessageBox.information(self, "Sukses", "Data berhasil disimpan!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan data: {str(e)}")

    def load_data(self):
        try:
            self.cursor.execute("SELECT * FROM books ORDER BY id DESC")
            records = self.cursor.fetchall()
            self.display_data(records)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data: {str(e)}")

    def display_data(self, records):
        self.table.blockSignals(True)
        self.table.setRowCount(len(records))
        
        for row_number, row_data in enumerate(records):
            for col_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                # Set font size for each item
                font = item.font()
                font.setPointSize(14)
                item.setFont(font)
                
                if col_number == 0:  # ID column - read only
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.table.setItem(row_number, col_number, item)
                
        self.table.blockSignals(False)

    def search_data(self, text):
        if text.strip():
            self.cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY id DESC", 
                              (f'%{text}%', f'%{text}%'))
        else:
            self.cursor.execute("SELECT * FROM books ORDER BY id DESC")
        
        records = self.cursor.fetchall()
        self.display_data(records)

    def update_data(self, row, column):
        if column == 0:  # Don't allow editing ID
            return
            
        try:
            book_id = int(self.table.item(row, 0).text())
            new_value = self.table.item(row, column).text().strip()
            
            if not new_value:
                QMessageBox.warning(self, "Peringatan", "Field tidak boleh kosong.")
                self.load_data()
                return
            
            column_name = ["id", "title", "author", "year"][column]
            
            if column_name == "year" and not new_value.isdigit():
                QMessageBox.warning(self, "Peringatan", "Tahun harus berupa angka.")
                self.load_data()
                return
            
            value = int(new_value) if column_name == "year" else new_value
            
            self.cursor.execute(f"UPDATE books SET {column_name} = ? WHERE id = ?", 
                              (value, book_id))
            self.conn.commit()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengupdate data: {str(e)}")
            self.load_data()

    def delete_data(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih baris yang ingin dihapus.")
            return
        
        try:    
            book_id = int(self.table.item(selected_row, 0).text())
            title = self.table.item(selected_row, 1).text()
            
            reply = QMessageBox.question(self, "Konfirmasi", 
                                       f"Apakah Anda yakin ingin menghapus buku '{title}'?",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
                self.conn.commit()
                self.load_data()
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menghapus data: {str(e)}")

    def export_data(self):
        try:
            path, _ = QFileDialog.getSaveFileName(self, "Simpan CSV", "books.csv", "CSV Files (*.csv)")
            if path:
                with open(path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Judul", "Pengarang", "Tahun"])
                    
                    self.cursor.execute("SELECT * FROM books ORDER BY id")
                    records = self.cursor.fetchall()
                    writer.writerows(records)
                    
                QMessageBox.information(self, "Ekspor Berhasil", 
                                      f"Data berhasil diekspor ke {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengekspor data: {str(e)}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = BookManager()
    window.show()
    
    sys.exit(app.exec_())