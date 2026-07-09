import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
from io import BytesIO
from database import Database


class HistoryWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('history.ui', self)
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_delete.clicked.connect(self.delete_selected)
        self.btn_clear_all.clicked.connect(self.clear_all)
        self.btn_close.clicked.connect(self.close)
        self.db = Database()
        self.setup_table()
        self.load_data()
        self.statusBar.showMessage('Готово')

    def setup_table(self):
        self.table_history.setColumnHidden(0, True)
        header = self.table_history.horizontalHeader()
        for i in range(self.table_history.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        self.table_history.setColumnWidth(6, 60)

    def load_data(self):
        records = self.db.get_all_records()
        self.table_history.setRowCount(len(records))
        for row, record in enumerate(records):
            self.table_history.setItem(row, 0, QTableWidgetItem(str(record[0])))
            self.table_history.setItem(row, 1, QTableWidgetItem(f'{record[1]:.2f} м'))
            self.table_history.setItem(row, 2, QTableWidgetItem(f'{record[2]:.2f} кг'))
            self.table_history.setItem(row, 3, QTableWidgetItem(f'{record[3]:.1f}'))
            self.table_history.setItem(row, 4, QTableWidgetItem(record[4]))
            self.table_history.setItem(row, 5, QTableWidgetItem(str(record[5])))
            image_path = record[6]
            if image_path and os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    img.thumbnail((40, 40), Image.Resampling.LANCZOS)
                    buffer = BytesIO()
                    img.save(buffer, format='PNG')
                    buffer.seek(0)
                    pixmap = QPixmap()
                    pixmap.loadFromData(buffer.getvalue())
                    item = QTableWidgetItem('')
                    item.setData(Qt.DecorationRole, pixmap)
                    self.table_history.setItem(row, 6, item)
                except Exception:
                    self.table_history.setItem(row, 6, QTableWidgetItem(''))
            else:
                self.table_history.setItem(row, 6, QTableWidgetItem(''))
        count = self.db.get_count()
        self.label_count.setText(f'Всего записей: {count}')
        self.statusBar.showMessage(f'Загружено записей: {len(records)}')

    def delete_selected(self):
        selected_row = self.table_history.currentRow()
        if selected_row == -1:
            QMessageBox.information(self, 'Информация', 'Выберите запись для удаления')
            return
        record_id = int(self.table_history.item(selected_row, 0).text())
        reply = QMessageBox.question(
            self,
            'Подтверждение удаления',
            'Вы уверены, что хотите удалить эту запись?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db.delete_record(record_id)
            self.load_data()
            self.statusBar.showMessage('Запись удалена', 3000)

    def clear_all(self):
        count = self.db.get_count()
        if count == 0:
            QMessageBox.information(self, 'Информация', 'История пуста')
            return
        reply = QMessageBox.question(
            self,
            'Подтверждение очистки',
            'Вы уверены, что хотите удалить все записи?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db.clear_history()
            self.load_data()
            self.statusBar.showMessage('История очищена', 3000)

    def closeEvent(self, event):
        self.db.close()
        event.accept()
