import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QShortcut
from PyQt5.QtGui import QPixmap, QKeySequence
from PIL import Image
from io import BytesIO
from database import Database
from ui_history import HistoryWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.btn.clicked.connect(self.calculate_bmi)
        self.units.currentIndexChanged.connect(self.change_units)
        self.db = Database()
        self.set_metric_units()
        self.set_default_image()
        self.action_history.triggered.connect(self.open_history)
        self.action_exit.triggered.connect(self.close)
        self.setup_shortcuts()

    def set_metric_units(self):
        self.height.setSingleStep(0.1)
        self.weight.setSingleStep(0.1)
        self.height.setDecimals(2)
        self.weight.setDecimals(2)
        self.label_height.setText('Рост, м:')
        self.label_weight.setText('Вес, кг:')

    def set_imperial_units(self):
        self.height.setSingleStep(0.1)
        self.weight.setSingleStep(1)
        self.height.setDecimals(2)
        self.weight.setDecimals(0)
        self.label_height.setText('Рост, футы:')
        self.label_weight.setText('Вес, фунты:')

    def change_units(self):
        system = self.units.currentText()
        if system == 'Международная (м, кг)':
            self.set_metric_units()
        else:
            self.set_imperial_units()
        self.height.setValue(0)
        self.weight.setValue(0)

    def calculate_bmi(self):
        try:
            height_raw = self.height.value()
            weight_raw = self.weight.value()
            height_value = float(str(height_raw).replace(',','.'))
            weight_value = float(str(weight_raw).replace(',','.'))
        except ValueError:
            self.result.setText('')
            self.state.setText('Ошибка ввода')
            return
        system = self.units.currentText()
        if height_value == 0 or weight_value == 0:
            self.result.setText('')
            self.state.setText('Введите рост и вес!')
            return
        if system == 'Международная (м, кг)':
            height_m = height_value
            weight_kg = weight_value
            bmi = weight_kg / (height_m ** 2)
        else:
            height_m = height_value * 0.3048
            weight_kg = weight_value * 0.4536
            bmi = weight_kg / (height_m ** 2)
        if bmi < 18.5:
            category = 'Дефицит массы тела'
        elif bmi < 25:
            category = 'Нормальный вес'
        elif bmi < 30:
            category = 'Избыточный вес'
        else:
            category = 'Ожирение'
        image_map = {
            'Дефицит массы тела': 'assets/underweight.png',
            'Нормальный вес': 'assets/normal.png',
            'Избыточный вес': 'assets/overweight.png',
            'Ожирение': 'assets/obesity.png'
        }
        image_path = image_map.get(category, 'assets/underweight.png')
        self.db.add_record(
            height=height_m,
            weight=weight_kg,
            bmi=bmi,
            category=category,
            image_path=image_path
        )
        self.result.setText(f'{bmi:.1f}')
        self.state.setText(category)
        self.set_result_image(category)

    def set_default_image(self):
        default_image_path = 'assets/underweight.png'
        if os.path.exists(default_image_path):
            try:
                img = Image.open(default_image_path)
                img.thumbnail((236, 500), Image.Resampling.LANCZOS)
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                pixmap = QPixmap()
                pixmap.loadFromData(buffer.getvalue())
                self.image.setPixmap(pixmap)
                return
            except Exception:
                pass

    def set_result_image(self, category):
        image_map = {
            'Дефицит массы тела': 'assets/underweight.png',
            'Нормальный вес': 'assets/normal.png',
            'Избыточный вес': 'assets/overweight.png',
            'Ожирение': 'assets/obesity.png'
        }
        image_path = image_map.get(category, 'assets/underweight.png')
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                label_width = self.image.width()
                label_height = self.image.height()
                img.thumbnail((label_width, label_height), Image.Resampling.LANCZOS)
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                pixmap = QPixmap()
                pixmap.loadFromData(buffer.getvalue())
                self.image.setPixmap(pixmap)
                self.image.setStyleSheet('')
                return
            except Exception:
                pass

    def open_history(self):
        self.history_window = HistoryWindow(self)
        self.history_window.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Подтверждение выхода',
            'Вы уверены, что хотите выйти?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def setup_shortcuts(self):
        shortcut_history = QShortcut(QKeySequence('Ctrl+H'), self)
        shortcut_history.activated.connect(self.open_history)
        self.action_history.setShortcut('Ctrl+H')
        shortcut_exit = QShortcut(QKeySequence('Ctrl+Q'), self)
        shortcut_exit.activated.connect(self.close)
        self.action_exit.setShortcut('Ctrl+Q')
        shortcut_enter = QShortcut(QKeySequence('Return'), self)
        shortcut_enter.activated.connect(self.btn.click)
