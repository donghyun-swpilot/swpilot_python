

import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit
)
from PyQt5.QtCore import Qt


class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current = ''
        self.operator = ''
        self.operand = ''
        self.result = ''

    def input_number(self, value):
        if value == '.' and '.' in self.current:
            return
        self.current += value

    def set_operator(self, op):
        if self.current == '':
            return
        self.operand = self.current
        self.operator = op
        self.current = ''

    def negative_positive(self):
        if self.current:
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current

    def percent(self):
        if self.current:
            try:
                self.current = str(float(self.current) / 100)
            except:
                self.current = 'Error'

    def equal(self):
        if self.operand and self.current:
            try:
                a = float(self.operand)
                b = float(self.current)
                if self.operator == '+':
                    self.result = str(a + b)
                elif self.operator == '-':
                    self.result = str(a - b)
                elif self.operator == 'x':
                    self.result = str(a * b)
                elif self.operator == '/':
                    self.result = str(a / b) if b != 0 else 'Error'
                else:
                    self.result = 'Error'
                self.current = self.result
                self.operator = ''
                self.operand = ''
            except:
                self.current = 'Error'


class EngineeringCalculator(Calculator):
    def sin(self):
        try:
            self.current = str(math.sin(math.radians(float(self.current))))
        except:
            self.current = 'Error'

    def cos(self):
        try:
            self.current = str(math.cos(math.radians(float(self.current))))
        except:
            self.current = 'Error'

    def tan(self):
        try:
            self.current = str(math.tan(math.radians(float(self.current))))
        except:
            self.current = 'Error'

    def sinh(self):
        try:
            self.current = str(math.sinh(float(self.current)))
        except:
            self.current = 'Error'

    def cosh(self):
        try:
            self.current = str(math.cosh(float(self.current)))
        except:
            self.current = 'Error'

    def tanh(self):
        try:
            self.current = str(math.tanh(float(self.current)))
        except:
            self.current = 'Error'

    def square(self):
        try:
            self.current = str(float(self.current) ** 2)
        except:
            self.current = 'Error'

    def cube(self):
        try:
            self.current = str(float(self.current) ** 3)
        except:
            self.current = 'Error'

    def pi(self):
        self.current = str(math.pi)


class EngineeringCalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("공학용 계산기")
        self.setFixedSize(350, 500)
        self.calc = EngineeringCalculator()
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(60)
        self.display.setStyleSheet("font-size: 24px;")
        vbox.addWidget(self.display)

        grid = QGridLayout()
        vbox.addLayout(grid)

        buttons = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '='],
            ['sin', 'cos', 'tan', 'π'],
            ['sinh', 'cosh', 'tanh', '^2'],
            ['^3']
        ]

        positions = [(i, j) for i in range(len(buttons)) for j in range(len(buttons[i]))]
        for position, text in zip(positions, sum(buttons, [])):
            button = QPushButton(text)
            button.setFixedHeight(50)
            button.setStyleSheet("font-size: 18px;")
            button.clicked.connect(self.button_clicked)
            grid.addWidget(button, *position)

    def button_clicked(self):
        text = self.sender().text()

        if text == 'AC':
            self.calc.reset()
        elif text == '+/-':
            self.calc.negative_positive()
        elif text == '%':
            self.calc.percent()
        elif text in ['+', '-', 'x', '/']:
            self.calc.set_operator(text)
        elif text == '=':
            self.calc.equal()
        elif text == '.':
            self.calc.input_number(text)
        elif text == '^2':
            self.calc.square()
        elif text == '^3':
            self.calc.cube()
        elif text == 'π':
            self.calc.pi()
        elif text == 'sin':
            self.calc.sin()
        elif text == 'cos':
            self.calc.cos()
        elif text == 'tan':
            self.calc.tan()
        elif text == 'sinh':
            self.calc.sinh()
        elif text == 'cosh':
            self.calc.cosh()
        elif text == 'tanh':
            self.calc.tanh()
        elif text.isdigit():
            self.calc.input_number(text)

        self.display.setText(self.calc.current)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EngineeringCalculatorApp()
    window.show()
    sys.exit(app.exec_())
