import sys
import sqlite3
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox,
    QHeaderView, QMenuBar, QMenu, QAction, QFrame, QMainWindow, QDockWidget,
    QStatusBar, QScrollArea, QTextEdit, QSplitter
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QClipboard

class BookManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manajemen Buku")
        self.resize(1000, 700)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                font-family: 'SF Pro Display', 'Segoe UI', Arial, sans-serif;
            }
            
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
            
            QPushButton#clipboardButton {
                background-color: #FFA726;
            }
            
            QPushButton#clipboardButton:hover {
                background-color: #FF9800;
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
            
            QDockWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                titlebar-close-icon: url(close.png);
                titlebar-normal-icon: url(float.png);
            }
            
            QDockWidget::title {
                text-align: left;
                background-color: #e9ecef;
                padding: 8px 12px;
                border-bottom: 1px solid #dee2e6;
                font-weight: 600;
                color: #495057;
            }
            
            QStatusBar {
                background-color: #e9ecef;
                border-top: 1px solid #dee2e6;
                padding: 4px;
                color: #495057;
                font-size: 12px;
            }
            
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                font-size: 12px;
                line-height: 1.4;
            }
            
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        # Initialize database connection
        self.conn = sqlite3.connect("books.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Initialize clipboard
        self.clipboard = QApplication.clipboard()

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
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.create_status_bar()
        
        # Create dock widgets
        self.create_dock_widgets()
        
        # Create central widget with scroll area
        self.create_central_widget()

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
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
        edit_menu = menubar.addMenu("Edit")
        
        delete_action = QAction("Hapus Data", self)
        delete_action.triggered.connect(self.delete_data)
        edit_menu.addAction(delete_action)
        
        paste_action = QAction("Paste dari Clipboard", self)
        paste_action.triggered.connect(self.paste_from_clipboard)
        edit_menu.addAction(paste_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        toggle_search_dock = QAction("Toggle Search Panel", self)
        toggle_search_dock.triggered.connect(self.toggle_search_dock)
        view_menu.addAction(toggle_search_dock)
        
        toggle_help_dock = QAction("Toggle Help Panel", self)
        toggle_help_dock.triggered.connect(self.toggle_help_dock)
        view_menu.addAction(toggle_help_dock)
        
        # Data menu
        data_menu = menubar.addMenu("Data Buku")
        
        add_action = QAction("Data Buku", self)
        data_menu.addAction(add_action)
        
        export_submenu = data_menu.addMenu("Ekspor")
        
        csv_action = QAction("CSV", self)
        csv_action.triggered.connect(self.export_data)
        export_submenu.addAction(csv_action)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Nama: Muhammad Rifkyandryan Rustanto | NIM: F1D022077")

    def create_dock_widgets(self):
        # Search dock widget
        self.search_dock = QDockWidget("Panel Pencarian", self)
        search_widget = QWidget()
        search_layout = QVBoxLayout(search_widget)
        
        search_label = QLabel("Cari Judul atau Pengarang:")
        search_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik untuk mencari...")
        self.search_input.textChanged.connect(self.search_data)
        
        clear_search_btn = QPushButton("Clear")
        clear_search_btn.clicked.connect(self.clear_search)
        clear_search_btn.setMaximumWidth(60)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(clear_search_btn)
        search_layout.addStretch()
        
        self.search_dock.setWidget(search_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.search_dock)
        
        # Help dock widget
        self.help_dock = QDockWidget("Panel Bantuan", self)
        help_widget = QWidget()
        help_layout = QVBoxLayout(help_widget)
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_content = """
<h3>Panduan Penggunaan Aplikasi Manajemen Buku</h3>

<h4>Menambah Data Buku:</h4>
<p>1. Isi form Judul, Pengarang, dan Tahun<br>
2. Klik tombol "Simpan"<br>
3. Data akan muncul di tabel</p>

<h4>Menggunakan Clipboard:</h4>
<p>1. Copy teks dari aplikasi lain<br>
2. Klik field yang ingin diisi<br>
3. Klik tombol "Paste" atau gunakan menu Edit</p>

<h4>Mencari Data:</h4>
<p>1. Gunakan panel pencarian di sebelah kiri<br>
2. Ketik judul atau nama pengarang<br>
3. Tabel akan menampilkan hasil pencarian</p>

<h4>Mengedit Data:</h4>
<p>1. Double-click pada cell yang ingin diedit<br>
2. Ubah nilai dan tekan Enter<br>
3. Data akan tersimpan otomatis</p>

<h4>Menghapus Data:</h4>
<p>1. Pilih baris yang ingin dihapus<br>
2. Klik tombol "Hapus Data"<br>
3. Konfirmasi penghapusan</p>

<h4>Ekspor Data:</h4>
<p>1. Klik tombol "Ekspor CSV"<br>
2. Pilih lokasi penyimpanan<br>
3. File CSV akan tersimpan</p>

<h4>Dock Panels:</h4>
<p>Panel ini dapat dipindah, dilepas, atau disembunyikan sesuai kebutuhan Anda.</p>
        """
        help_text.setHtml(help_content)
        
        help_layout.addWidget(help_text)
        
        self.help_dock.setWidget(help_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.help_dock)

    def create_central_widget(self):
        # Create scroll area for the main content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        content_widget = QWidget()
        content_widget.setMinimumSize(800, 600)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Manajemen Buku")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                margin: 15px 0;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
            }
        """)
        content_layout.addWidget(title_label)
        
        # Input form frame
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 25px;
                border: 1px solid #e0e0e0;
        
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        
        # Input fields with clipboard integration
        input_layout = QHBoxLayout()
        input_layout.setSpacing(15)
        
        # Title input with clipboard
        title_container = QVBoxLayout()
        title_container.addWidget(QLabel("Judul:"))
        title_input_layout = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setMaximumWidth(150)
        paste_title_btn = QPushButton("📋")
        paste_title_btn.setObjectName("clipboardButton")
        paste_title_btn.setMaximumWidth(30)
        paste_title_btn.setToolTip("Paste dari clipboard")
        paste_title_btn.clicked.connect(lambda: self.paste_to_field(self.title_input))
        title_input_layout.addWidget(self.title_input)
        title_input_layout.addWidget(paste_title_btn)
        title_container.addLayout(title_input_layout)
        input_layout.addLayout(title_container)
        
        # Author input with clipboard
        author_container = QVBoxLayout()
        author_container.addWidget(QLabel("Pengarang:"))
        author_input_layout = QHBoxLayout()
        self.author_input = QLineEdit()
        self.author_input.setMaximumWidth(150)
        paste_author_btn = QPushButton("📋")
        paste_author_btn.setObjectName("clipboardButton")
        paste_author_btn.setMaximumWidth(30)
        paste_author_btn.setToolTip("Paste dari clipboard")
        paste_author_btn.clicked.connect(lambda: self.paste_to_field(self.author_input))
        author_input_layout.addWidget(self.author_input)
        author_input_layout.addWidget(paste_author_btn)
        author_container.addLayout(author_input_layout)
        input_layout.addLayout(author_container)
        
        # Year input with clipboard
        year_container = QVBoxLayout()
        year_container.addWidget(QLabel("Tahun:"))
        year_input_layout = QHBoxLayout()
        self.year_input = QLineEdit()
        self.year_input.setMaximumWidth(100)
        paste_year_btn = QPushButton("📋")
        paste_year_btn.setObjectName("clipboardButton")
        paste_year_btn.setMaximumWidth(30)
        paste_year_btn.setToolTip("Paste dari clipboard")
        paste_year_btn.clicked.connect(lambda: self.paste_to_field(self.year_input))
        year_input_layout.addWidget(self.year_input)
        year_input_layout.addWidget(paste_year_btn)
        year_container.addLayout(year_input_layout)
        input_layout.addLayout(year_container)
        
        # Save button
        self.save_button = QPushButton("Simpan")
        self.save_button.setMaximumWidth(100)
        self.save_button.clicked.connect(self.save_data)
        input_layout.addWidget(self.save_button)
        
        input_layout.addStretch()
        
        form_layout.addLayout(input_layout)
        content_layout.addWidget(form_frame)
        
        # Table frame with scroll support
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;

            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Pengarang", "Tahun"])
        self.table.cellChanged.connect(self.update_data)
        self.table.setEditTriggers(QTableWidget.DoubleClicked)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        
        # Enable scrolling for table
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setMinimumHeight(350)
        
        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.verticalHeader().setVisible(False)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.resizeSection(0, 60)  
        header.setSectionResizeMode(1, QHeaderView.Stretch)  
        header.setSectionResizeMode(2, QHeaderView.Stretch)    
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.resizeSection(3, 80)  
        
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
        
        scroll_area.setWidget(content_widget)
        self.setCentralWidget(scroll_area)

    def paste_to_field(self, field):
        """Paste clipboard content to specific field"""
        clipboard_text = self.clipboard.text()
        if clipboard_text:
            field.setText(clipboard_text.strip())
            self.status_bar.showMessage(f"Teks berhasil di-paste: '{clipboard_text[:50]}...' | Nama: Muhammad Rifkyandryan Rustanto | NIM: F1D022077", 3000)
        else:
            QMessageBox.information(self, "Clipboard Kosong", "Tidak ada teks di clipboard.")

    def paste_from_clipboard(self):
        """Paste clipboard content to currently focused field"""
        focused = self.focusWidget()
        if isinstance(focused, QLineEdit):
            self.paste_to_field(focused)
        else:
            QMessageBox.information(self, "Info", "Pilih field input terlebih dahulu.")

    def toggle_search_dock(self):
        """Toggle search dock visibility"""
        if self.search_dock.isVisible():
            self.search_dock.hide()
        else:
            self.search_dock.show()

    def toggle_help_dock(self):
        """Toggle help dock visibility"""
        if self.help_dock.isVisible():
            self.help_dock.hide()
        else:
            self.help_dock.show()

    def clear_search(self):
        """Clear search input and reload all data"""
        self.search_input.clear()
        self.load_data()

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
            
            self.title_input.clear()
            self.author_input.clear()
            self.year_input.clear()
            
            self.load_data()
            QMessageBox.information(self, "Sukses", "Data berhasil disimpan!")
            self.status_bar.showMessage("Data baru berhasil ditambahkan | Nama: Muhammad Rifkyandryan Rustanto | NIM: F1D022077", 3000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan data: {str(e)}")

    def load_data(self):
        try:
            self.cursor.execute("SELECT * FROM books ORDER BY id DESC")
            records = self.cursor.fetchall()
            self.display_data(records)
            self.status_bar.showMessage(f"Menampilkan {len(records)} data buku | Nama: Muhammad Rifkyandryan Rustanto | NIM: F1D022077", 2000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data: {str(e)}")

    def display_data(self, records):
        self.table.blockSignals(True)
        self.table.setRowCount(len(records))
        
        for row_number, row_data in enumerate(records):
            for col_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                font = item.font()
                font.setPointSize(14)
                item.setFont(font)
                
                if col_number == 0:  
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.table.setItem(row_number, col_number, item)
                
        self.table.blockSignals(False)

    def search_data(self, text):
        if text.strip():
            self.cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY id DESC", 
                              (f'%{text}%', f'%{text}%'))
            records = self.cursor.fetchall()
            self.status_bar.showMessage(f"Pencarian: '{text}' - Ditemukan {len(records)} hasil | Nama: Muhammad Rifkyandryan Rustanto | NIM: F1D022077", 2000)
        else:
            self.cursor.execute("SELECT * FROM books ORDER BY id DESC")
            records = self.cursor.fetchall()
        
        self.display_data(records)

    def update_data(self, row, column):
        if column == 0: 
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
            self.status_bar.showMessage("Data berhasil diupdate | Nama: Muhammad Rifkyandryan Rustanto | NIM: F1D022077", 2000)
            
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
                self.status_bar.showMessage("Data berhasil dihapus | Nama: Muhammad Rifkyandryan Rustanto | NIM: F1D022077", 2000)
                
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
                self.status_bar.showMessage(f"Data berhasil diekspor ke CSV | Nama: Muhammad Rifkyandryan Rustanto | NIM: F1D022077", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengekspor data: {str(e)}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = BookManager()
    window.show()
    
    sys.exit(app.exec_())