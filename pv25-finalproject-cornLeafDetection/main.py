import sys
import os
import sqlite3
import joblib 
import cv2
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from skimage.feature import graycomatrix, graycoprops, local_binary_pattern

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class CornDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = os.path.join(os.path.dirname(__file__), 'main.ui')
        
        if not os.path.exists(ui_file_path):
            QMessageBox.critical(self, "Error", f"UI file not found at: {ui_file_path}")
            sys.exit(1)
            
        uic.loadUi(ui_file_path, self)
        
        self.current_image_path = None
        self.models = {}

        self.setupUI()
        self.loadModels()
        self.connectSignals()
        self.initDatabase()
        
    def setupUI(self):
        """Setup UI components after loading"""
        self.setWindowTitle('Aplikasi Deteksi Jagung - Machine Learning')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon)) 
        
        self.modelCombo.clear()
        models = [
            'COLOR_RF (Akurasi: 0.8247)',
            'LBP_RF (Akurasi: 0.7731)',
            'GLCM_RF (Akurasi: 0.7325)'
        ]
        self.modelCombo.addItems(models)
        
        self.filterCombo.clear()
        self.filterCombo.addItems(['Semua', 'Daun Jagung Baik', 'Daun Jagung Sakit', 'Bukan Daun Jagung'])
        
        self.table.setColumnCount(6)
        headers = ['ID', 'Nama File', 'Hasil Prediksi', 'Model', 'Tanggal', 'Confidence']
        self.table.setHorizontalHeaderLabels(headers)
        
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        
        self.table.verticalHeader().setVisible(True) 
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed) 
        self.table.verticalHeader().setDefaultSectionSize(40) 
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents) 
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)           
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents) 
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents) 
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents) 
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents) 
        self.table.horizontalHeader().setVisible(True)
        self.table.setMinimumHeight(250) 
        
        self.searchInput.setPlaceholderText('Cari berdasarkan nama file...')
        
        self.resultLabel.setText('-')
        self.confidenceLabel.setText('-')
        self.processingTimeLabel.setText('-')
        
        self.btnPredict.setEnabled(False)
        
    def connectSignals(self):
        """Connect UI signals to methods"""
        self.btnSelectImage.clicked.connect(self.selectImage)
        self.btnPredict.clicked.connect(self.predictImage)
        self.btnRefresh.clicked.connect(self.loadTableData)
        self.btnDelete.clicked.connect(self.deleteRecord)
        self.btnExportCSV.clicked.connect(self.exportToCSV)
        self.btnExportPDF.clicked.connect(self.exportToPDF)
        
        self.searchInput.textChanged.connect(self.filterResults)
        self.filterCombo.currentTextChanged.connect(self.filterResults)
        
        self.actionOpenImage.triggered.connect(self.selectImage) 
        self.actionExportCSV.triggered.connect(self.exportToCSV)
        self.actionExportPDF.triggered.connect(self.exportToPDF)
        self.actionExit.triggered.connect(self.close)
        self.actionRefresh.triggered.connect(self.loadTableData)
        self.actionAbout.triggered.connect(self.showAbout)
        


    def initDatabase(self):
        """Initialize SQLite database"""
        self.db_path = 'corn.db'
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                result TEXT NOT NULL,
                model_used TEXT NOT NULL,
                prediction_date TEXT NOT NULL,
                confidence REAL,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        self.loadTableData() 
        
    def loadModels(self):
        """Load machine learning models"""
        self.models = {}
        model_file_names = [
            'model_COLOR_RF.pkl',
            'model_LBP_RF.pkl', 
            'model_GLCM_RF.pkl'
        ]
        
        self.model_directory = os.path.dirname(__file__) 
        
        for model_file_name in model_file_names:
            model_full_path = os.path.join(self.model_directory, model_file_name)
            if os.path.exists(model_full_path):
                try:
                    self.models[model_full_path] = joblib.load(model_full_path)
                    print(f"Loaded model: {model_full_path}")
                except Exception as e:
                    print(f"Error loading {model_full_path}: {e}")
                    QMessageBox.warning(self, 'Warning', f"Gagal memuat model {model_file_name}: {e}")
            else:
                print(f"Model file not found: {model_full_path}")
        
        if not self.models:
            QMessageBox.warning(self, 'Warning', 'Tidak ada model yang ditemukan!\nPastikan file model (.pkl) ada di direktori yang benar.')
            
    def selectImage(self):
        """Select image file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Pilih Gambar Jagung', '', 
            'Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)'
        )
        
        if file_path:
            self.current_image_path = file_path
            
            pixmap = QPixmap(file_path)
            if self.imageLabel.width() > 0 and self.imageLabel.height() > 0:
                scaled_pixmap = pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.imageLabel.setPixmap(scaled_pixmap)
            else:
                self.imageLabel.setPixmap(pixmap) 
                self.imageLabel.adjustSize() 
            
            self.btnPredict.setEnabled(True)
            self.statusBar().showMessage(f'Gambar dipilih: {os.path.basename(file_path)}')

    def _extract_glcm_gui(self, gray_img_float):
        """Extract GLCM features"""
        gray_scaled_uint8 = (gray_img_float * 255).astype(np.uint8) 
        if gray_scaled_uint8.size == 0 or gray_scaled_uint8.ndim < 2:
            raise ValueError("Gambar kosong atau tidak valid untuk ekstraksi GLCM.")
        glcm = graycomatrix(gray_scaled_uint8, distances=[1], angles=[0], symmetric=True, normed=True)
        return [
            graycoprops(glcm, 'contrast')[0, 0],
            graycoprops(glcm, 'correlation')[0, 0],
            graycoprops(glcm, 'energy')[0, 0],
            graycoprops(glcm, 'homogeneity')[0, 0]
        ] 

    def _extract_lbp_gui(self, gray_img_float):
        """Extract LBP features"""
        if gray_img_float.size == 0 or gray_img_float.ndim < 2:
            raise ValueError("Gambar kosong atau tidak valid untuk ekstraksi LBP.")
        
        radius = 1
        points = 8 
        lbp = local_binary_pattern(gray_img_float, points, radius, method='uniform')
        hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, points + 3), range=(0, points + 2))
        return (hist / (hist.sum() + 1e-6)).tolist() 

    def _extract_color_gui(self, image_rgb_float):
        """Extract color features"""
        if image_rgb_float.size == 0 or image_rgb_float.ndim < 3:
            raise ValueError("Gambar kosong atau tidak valid untuk ekstraksi warna.")
            
        chans = cv2.split((image_rgb_float * 255).astype(np.uint8))
        features = []
        for chan in chans:
            hist = cv2.calcHist([chan], [0], None, [256], [0, 256]).flatten()
            features.extend(hist / (hist.sum() + 1e-6))
        return features 

    def extractFeatures(self, image_path, method_prefix):
        """Extract features from image based on method"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Cannot load image from {image_path}. Check file path and integrity.")

            image_resized = cv2.resize(image, (256, 256))

            image_rgb_float = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
            image_gray_float = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0

            features = []

            if method_prefix == 'GLCM':
                features.extend(self._extract_glcm_gui(image_gray_float))
            elif method_prefix == 'LBP':
                features.extend(self._extract_lbp_gui(image_gray_float))
            elif method_prefix == 'COLOR':
                features.extend(self._extract_color_gui(image_rgb_float))
            else:
                QMessageBox.warning(self, 'Warning', f"Metode ekstraksi fitur '{method_prefix}' tidak dikenal.")
                return None
            
            print(f"DEBUG: Extracted {len(features)} features for method {method_prefix}.")
            
            if not features:
                raise ValueError(f"Tidak ada fitur yang diekstrak untuk metode {method_prefix}.")
            
            return np.array(features).reshape(1, -1)
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            QMessageBox.critical(self, 'Error', f'Gagal mengekstrak fitur dari gambar:\n{str(e)}')
            return None
            
    def predictImage(self):
        """Predict image using selected model"""
        if not hasattr(self, 'current_image_path') or not self.current_image_path:
            QMessageBox.warning(self, 'Warning', 'Pilih gambar terlebih dahulu!')
            return
            
        selected_text = self.modelCombo.currentText()
        model_name_prefix = selected_text.split(' (')[0] 
        feature_method_type = model_name_prefix.split('_')[0] 
        
        model_full_path = os.path.join(self.model_directory, f"model_{model_name_prefix}.pkl")
        
        if not os.path.exists(model_full_path) or model_full_path not in self.models:
            QMessageBox.warning(self, 'Error', f'Model {model_name_prefix} ({model_full_path}) tidak tersedia atau gagal dimuat!')
            return
            
        try:
            start_time = datetime.now()
            
            features = self.extractFeatures(self.current_image_path, feature_method_type) 
            if features is None:
                return 
                
            model = self.models[model_full_path]
            prediction_numeric = model.predict(features)[0] 
            
            confidence = 0.0
            if hasattr(model, 'predict_proba'):
                try:
                    prob = model.predict_proba(features)[0]
                    confidence = np.max(prob)
                except Exception as e:
                    print(f"Warning: Could not get probability for model {model_name_prefix}: {e}")
                    
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            original_class_labels_map = {
                0: 'Bukan_Jagung',
                1: 'Corn_Cercospora_leaf_spot Gray_leaf_spot',
                2: 'Corn_Northern_Leaf_Blight',
                3: 'corn_healthy'
            }
            
            predicted_original_label = original_class_labels_map.get(prediction_numeric, 'UNKNOWN_CLASS')

            result_text = "UNKNOWN PREDICTION"
            
            if predicted_original_label == 'corn_healthy':
                result_text = 'Daun Jagung Baik'
            elif predicted_original_label in ['Corn_Cercospora_leaf_spot Gray_leaf_spot', 'Corn_Northern_Leaf_Blight']:
                result_text = 'Daun Jagung Sakit'
            elif predicted_original_label == 'Bukan_Jagung':
                result_text = 'Bukan Daun Jagung'
            else:
                result_text = f'Hasil Tidak Dikenal ({predicted_original_label})' 
       
            self.resultLabel.setText(result_text)
            self.confidenceLabel.setText(f'{confidence:.2%}')
            self.processingTimeLabel.setText(f'{processing_time:.3f} detik')
            
            self.saveToDatabase(
                os.path.basename(self.current_image_path),
                result_text,
                model_name_prefix,
                confidence
            )
            
            self.statusBar().showMessage(f'Prediksi selesai: {result_text} ({confidence:.2%})')
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Terjadi kesalahan saat prediksi:\n{str(e)}')
            self.statusBar().showMessage('Prediksi gagal')
            
    def saveToDatabase(self, filename, result, model, confidence):
        """Save prediction result to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (filename, result, model_used, prediction_date, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (filename, result, model, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), confidence, ''))
        
        conn.commit()
        conn.close()
        self.loadTableData() 
        
    def loadTableData(self):
        """Load data from database to table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM predictions ORDER BY id ASC')
        data = cursor.fetchall()
        
        self.table.setRowCount(len(data))
        


        for i, row in enumerate(data):
            for j, value in enumerate(row):
                if j == 5:  
                    item = QTableWidgetItem(f'{value:.2%}' if value is not None else '-')
                else:
                    item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  
                self.table.setItem(i, j, item)
        
        conn.close()
        
        self.table.resizeColumnsToContents()
        
        self.table.updateGeometry() 
        self.table.viewport().update()
            
    def filterResults(self):
        """Filter table results based on search and filter criteria"""
        search_text = self.searchInput.text().lower()
        filter_text = self.filterCombo.currentText()
        
        for i in range(self.table.rowCount()):
            show_row = True
            
            filename_item = self.table.item(i, 1)
            if filename_item and search_text:
                filename = filename_item.text().lower()
                if search_text not in filename:
                    show_row = False
            
            result_item = self.table.item(i, 2)
            if result_item and filter_text != 'Semua':
                result = result_item.text()
                if result != filter_text: 
                    show_row = False
            
            self.table.setRowHidden(i, not show_row)
            
    def deleteRecord(self):
        """Delete selected record from database"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'Warning', 'Pilih baris yang akan dihapus!')
            return
            
        reply = QMessageBox.question(self, 'Konfirmasi', 'Yakin ingin menghapus record ini?',
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            record_id_item = self.table.item(current_row, 0)
            if record_id_item:
                record_id = record_id_item.text()
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM predictions WHERE id = ?', (record_id,))
                conn.commit()
                conn.close()
                
                self.loadTableData()
                self.statusBar().showMessage('Record berhasil dihapus')
            else:
                QMessageBox.warning(self, 'Error', 'Tidak dapat mengambil ID record.')
                
    def exportToCSV(self):
        """Export data to CSV file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Export ke CSV', 'corn_detection_results.csv', 
            'CSV Files (*.csv)'
        )
        
        if file_path:
            try:
                conn = sqlite3.connect(self.db_path)
                df = pd.read_sql_query('SELECT * FROM predictions', conn)
                df.to_csv(file_path, index=False)
                conn.close()
                
                QMessageBox.information(self, 'Success', f'Data berhasil diekspor ke:\n{file_path}')
                self.statusBar().showMessage('Export CSV berhasil')
                
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Gagal mengekspor ke CSV:\n{str(e)}')
                
    def exportToPDF(self):
        """Export data to PDF file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Export ke PDF', 'corn_detection_results.pdf',
            'PDF Files (*.pdf)'
        )
        
        if file_path:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM predictions ORDER BY id DESC')
                data = cursor.fetchall()
                conn.close()
                
                doc = SimpleDocTemplate(file_path, pagesize=letter)
                elements = []
                
                styles = getSampleStyleSheet()
                title = Paragraph("Laporan Hasil Deteksi Jagung", styles['Title'])
                elements.append(title)
                elements.append(Paragraph("<br/><br/>", styles['Normal']))
                
                table_data = [['ID', 'Nama File', 'Hasil', 'Model', 'Tanggal', 'Confidence']]
                
                for row in data:
                    formatted_row = [
                        str(row[0]),
                        str(row[1]),
                        str(row[2]),
                        str(row[3]),
                        str(row[4]),
                        f'{row[5]:.2%}' if row[5] is not None else '-'
                    ]
                    table_data.append(formatted_row)
                
                table = Table(table_data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                elements.append(table)
                doc.build(elements)
                
                QMessageBox.information(self, 'Success', f'Data berhasil diekspor ke:\n{file_path}')
                self.statusBar().showMessage('Export PDF berhasil')
                
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Gagal mengekspor ke PDF:\n{str(e)}')
                
    def showAbout(self):
        """Show about dialog"""
        QMessageBox.about(self, 'Tentang Aplikasi',
                            '''
                            <h3>Aplikasi Deteksi Jagung</h3>
                            <p><b>Versi:</b> 1.0</p>
                            <p><b>Pengembang:</b> Muhammad Rifkyandryan Rustanto</p>
                            <p><b>NIM:</b> F1D022077</p>
                            <p><b>Program Studi:</b> Teknik Informatika</p>
                            <br>
                            <p>Aplikasi ini menggunakan Machine Learning untuk mendeteksi kondisi jagung berdasarkan gambar.</p>
                            <p><b>Model yang tersedia:</b></p>
                            <ul>
                            <li>COLOR + Random Forest (82.47%)</li>
                            <li>LBP + Random Forest (77.31%)</li>
                            <li>GLCM + Random Forest (73.25%)</li>
                            </ul>
                            ''')

def main():
    app = QApplication(sys.argv)
    window = CornDetectionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()