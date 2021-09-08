from PyQt5 import QtCore
from data import Data
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from data import Data
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

class ClickableLineEdit(QLineEdit):
    clicked = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.clear_text)
    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()
    def clear_text(self):
        self.clear()
        self.setStyleSheet('font-size:14px')


class SettingWindow(QDialog):
    def __init__(self, data: Data, parent=None):
        super().__init__(parent)

        self.data = data
        # generate all widgets for the setting window
        self.darkcounts_widget = QWidget()
        self.darkcounts_box = ClickableLineEdit()
        self.darkcounts_label = QLabel()
        # self.set_darkcounts_style()

        self.core_percent_widget = QWidget()
        self.core_percent_box = ClickableLineEdit()
        self.core_percent_label = QLabel()
        # self.set_core_percent_style()

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # set layouts
        self.set_darkcounts_layout()
        self.set_core_percent_layout()
        self.set_whole_window_layout()

        # set_style
        self.set_core_percent_style()
        self.set_darkcounts_style()
        self.set_style()

        # add click button call back funcs
        self.button_box.accepted.connect(self.handle_confirm)
        self.button_box.rejected.connect(self.handle_reject)
    
    def set_darkcounts_style(self):
        self.darkcounts_label.setFixedWidth(200)
        self.darkcounts_label.setText('<html><ul><li>Dark Counts</li></ul></html>')
        self.darkcounts_label.setStyleSheet('font-size:14px; font-weight:bold')
        self.darkcounts_box.setText('Integer only')
        self.darkcounts_box.setStyleSheet('color:grey; font-size:13px')
        self.darkcounts_box.setValidator(QIntValidator())

    def set_core_percent_style(self):
        self.core_percent_label.setFixedWidth(200)
        self.core_percent_label.setText('<html><ul><li>Core Usage Percent</li></ul></html>')
        self.core_percent_label.setStyleSheet('font-size:14px; font-weight:bold')
        self.core_percent_box.setText('Decimal Number from 0-1')
        self.core_percent_box.setStyleSheet('color:grey; font-size:13px')
        self.core_percent_box.setValidator(QDoubleValidator())

    def set_darkcounts_layout(self):
        darkcounts_layout = QHBoxLayout()
        darkcounts_layout.addWidget(self.darkcounts_label)
        darkcounts_layout.addWidget(self.darkcounts_box)
        self.darkcounts_widget.setLayout(darkcounts_layout)
        
    def set_core_percent_layout(self):
        core_percent_layout = QHBoxLayout()
        core_percent_layout.addWidget(self.core_percent_label)
        core_percent_layout.addWidget(self.core_percent_box)
        self.core_percent_widget.setLayout(core_percent_layout)

    def set_whole_window_layout(self):
        whole_window_layout = QVBoxLayout()
        whole_window_layout.addWidget(self.darkcounts_widget)
        whole_window_layout.addWidget(self.core_percent_widget)
        whole_window_layout.addWidget(self.button_box)
        self.setLayout(whole_window_layout)

    def set_style(self):
        self.setFixedWidth(500)
        self.setWindowTitle('Settings')

    def handle_confirm(self):
        input_darkcounts = self.darkcounts_box.text()
        input_cpu = self.core_percent_box.text()
        if input_darkcounts:
            self.data.darkcount = int(self.darkcounts_box.text())
        if input_cpu and 0 < float(input_cpu) <= 1:
            self.data.core_percent = float(self.core_percent_box.text())
        self.close()
    
    def handle_reject(self):
        self.close()
