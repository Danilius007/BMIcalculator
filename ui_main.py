from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.btn.clicked.connect(self.calculate_bmi)
        self.units.currentIndexChanged.connect(self.change_units)
        self.set_metric_units()

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
