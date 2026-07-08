import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from PIL import Image
from io import  BytesIO

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.btn.clicked.connect(self.calculate_bmi)
        self.units.currentIndexChanged.connect(self.change_units)
        self.set_metric_units()
        self.set_default_image()

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
        height_value = self.height.value()
        weight_value = self.weight.value()
        system = self.units.currentText()
        if height_value == 0 or weight_value == 0:
            self.result.setText('')
            self.state.setText('Введите рост и вес!')
            return
        if system == 'Международная (м, кг)':
            height_m = height_value
            weight_kg = weight_value
            bmi = weight_kg/(height_m ** 2)
        else:
            height_inch = height_value * 12
            bmi = (weight_value * 703)/(height_inch ** 2)
        if bmi < 18.5:
            category = 'Дефицит массы тела'
        elif bmi < 25:
            category = 'Нормальный вес'
        elif bmi < 30:
            category = 'Избыточный вес'
        else:
            category = 'Ожирение'
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
            except Exception as e:
                print(f'Ошибка загрузки картинки: {e}')

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
            except Exception as e:
                print(f'Ошибка загрузки картинки: {e}')