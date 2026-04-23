import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QWidget


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.current_value = '0'
        self.stored_value = None
        self.pending_operator = None
        self.waiting_for_number = False

        self.setWindowTitle('Calculator')
        self.setFixedSize(360, 560)
        self.setStyleSheet('background-color: #000000;')

        self.display = QLabel(self.current_value)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet(
            'color: #ffffff;'
            'font-size: 58px;'
            'font-weight: 300;'
            'padding: 20px 18px 8px 18px;'
        )

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 24, 12, 12)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.display, 1)

        button_layout = QGridLayout()
        button_layout.setSpacing(10)
        self.add_buttons(button_layout)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def add_buttons(self, layout):
        buttons = [
            ('AC', 0, 0, 1, 1, 'function'),
            ('+/-', 0, 1, 1, 1, 'function'),
            ('%', 0, 2, 1, 1, 'function'),
            ('÷', 0, 3, 1, 1, 'operator'),
            ('7', 1, 0, 1, 1, 'number'),
            ('8', 1, 1, 1, 1, 'number'),
            ('9', 1, 2, 1, 1, 'number'),
            ('×', 1, 3, 1, 1, 'operator'),
            ('4', 2, 0, 1, 1, 'number'),
            ('5', 2, 1, 1, 1, 'number'),
            ('6', 2, 2, 1, 1, 'number'),
            ('-', 2, 3, 1, 1, 'operator'),
            ('1', 3, 0, 1, 1, 'number'),
            ('2', 3, 1, 1, 1, 'number'),
            ('3', 3, 2, 1, 1, 'number'),
            ('+', 3, 3, 1, 1, 'operator'),
            ('0', 4, 0, 1, 2, 'number'),
            ('.', 4, 2, 1, 1, 'number'),
            ('=', 4, 3, 1, 1, 'operator'),
        ]

        for text, row, column, row_span, column_span, button_type in buttons:
            button = QPushButton(text)
            button.setCursor(Qt.PointingHandCursor)
            button.setFixedHeight(68)
            button.setStyleSheet(self.get_button_style(button_type, column_span))
            button.clicked.connect(lambda checked, value=text: self.handle_click(value))
            layout.addWidget(button, row, column, row_span, column_span)

    def get_button_style(self, button_type, column_span):
        radius = 34
        padding_left = 24 if column_span == 2 else 0
        text_align = 'text-align: left;' if column_span == 2 else ''

        if button_type == 'operator':
            color = '#ff9500'
            pressed_color = '#d87d00'
            text_color = '#ffffff'
        elif button_type == 'function':
            color = '#a5a5a5'
            pressed_color = '#8f8f8f'
            text_color = '#000000'
        else:
            color = '#333333'
            pressed_color = '#555555'
            text_color = '#ffffff'

        return (
            'QPushButton {'
            f'background-color: {color};'
            f'color: {text_color};'
            'border: none;'
            f'border-radius: {radius}px;'
            'font-size: 28px;'
            f'padding-left: {padding_left}px;'
            f'{text_align}'
            '}'
            'QPushButton:pressed {'
            f'background-color: {pressed_color};'
            '}'
        )

    def handle_click(self, value):
        if value.isdigit():
            self.input_digit(value)
        elif value == '.':
            self.input_decimal_point()
        elif value == 'AC':
            self.clear()
        elif value == '+/-':
            self.toggle_sign()
        elif value == '%':
            self.convert_to_percent()
        elif value in ('+', '-', '×', '÷'):
            self.set_operator(value)
        elif value == '=':
            self.calculate()

        self.update_display()

    def input_digit(self, digit):
        if self.waiting_for_number or self.current_value == '0':
            self.current_value = digit
            self.waiting_for_number = False
        else:
            self.current_value += digit

    def input_decimal_point(self):
        if self.waiting_for_number:
            self.current_value = '0'
            self.waiting_for_number = False

        if '.' not in self.current_value:
            self.current_value += '.'

    def clear(self):
        self.current_value = '0'
        self.stored_value = None
        self.pending_operator = None
        self.waiting_for_number = False

    def toggle_sign(self):
        if self.current_value == '0':
            return

        if self.current_value.startswith('-'):
            self.current_value = self.current_value[1:]
        else:
            self.current_value = '-' + self.current_value

    def convert_to_percent(self):
        value = float(self.current_value) / 100
        self.current_value = self.format_number(value)

    def set_operator(self, operator):
        if self.pending_operator and not self.waiting_for_number:
            self.calculate()

        self.stored_value = float(self.current_value)
        self.pending_operator = operator
        self.waiting_for_number = True

    def calculate(self):
        if self.pending_operator is None or self.stored_value is None:
            return

        right_value = float(self.current_value)

        if self.pending_operator == '+':
            result = self.stored_value + right_value
        elif self.pending_operator == '-':
            result = self.stored_value - right_value
        elif self.pending_operator == '×':
            result = self.stored_value * right_value
        elif self.pending_operator == '÷':
            if right_value == 0:
                self.current_value = 'Error'
                self.stored_value = None
                self.pending_operator = None
                self.waiting_for_number = True
                return
            result = self.stored_value / right_value

        self.current_value = self.format_number(result)
        self.stored_value = None
        self.pending_operator = None
        self.waiting_for_number = True

    def format_number(self, value):
        if value.is_integer():
            return str(int(value))

        return str(round(value, 10)).rstrip('0').rstrip('.')

    def update_display(self):
        if len(self.current_value) > 9:
            self.display.setStyleSheet(
                'color: #ffffff;'
                'font-size: 42px;'
                'font-weight: 300;'
                'padding: 20px 18px 8px 18px;'
            )
        else:
            self.display.setStyleSheet(
                'color: #ffffff;'
                'font-size: 58px;'
                'font-weight: 300;'
                'padding: 20px 18px 8px 18px;'
            )

        self.display.setText(self.current_value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
