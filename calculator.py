import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setFixedSize(300, 400)
        self.init_ui()
        self.expression = ''

    def init_ui(self):
        vbox = QVBoxLayout()

        # Display
        self.display = QLabel('')
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 30px; padding: 10px; background-color: black; color: white;")
        vbox.addWidget(self.display)

        # Buttons
        grid = QGridLayout()
        buttons = [
            ['⌫', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['\U0001f4c8', '0', '.', '=']
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                btn = QPushButton(btn_text)
                btn.setFixedSize(60, 60)

                # 색상 지정
                if col_idx == 3:
                    color = '#f1a33c'  # 노란색
                elif row_idx == 0 and col_idx in [0, 1, 2]:
                    color = '#a5a5a5'  # 회색
                else:
                    color = '#333'     # 검은색

                btn.setStyleSheet(f"""
                    font-size: 18px;
                    border-radius: 30px;
                    background-color: {color};
                    color: white;
                """)
                btn.clicked.connect(self.on_button_clicked)
                grid.addWidget(btn, row_idx, col_idx)

        vbox.addLayout(grid)
        self.setLayout(vbox)

    def on_button_clicked(self):
        button = self.sender()
        text = button.text()

        if text == '⌫':
            self.expression = self.expression[:-1]
        elif text == '=':
            try:
                self.expression = str(eval(self.expression))
            except Exception:
                self.expression = 'Error'
        elif text == '+/-':
            if self.expression and self.expression[0] == '-':
                self.expression = self.expression[1:]
            elif self.expression:
                self.expression = '-' + self.expression
        elif text == '%':
            try:
                self.expression = str(eval(self.expression) / 100)
            except Exception:
                self.expression = 'Error'
        elif text in ['+', '-', '*', '/', '.'] or text.isdigit():
            self.expression += text
        else:
            pass

        self.display.setText(self.expression)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
