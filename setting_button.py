from data import Data
from PyQt5.QtWidgets import QInputDialog, QPushButton
from setting_window import SettingWindow
from PyQt5.QtCore import Qt


class SettingButton(QPushButton):

    def __init__(self, name: str, data: Data):
        super().__init__(name)
        self.data = data
        self.clicked.connect(self.handle_click_setting_button)
    
    def handle_click_setting_button(self):
        setting_window = SettingWindow(self.data)
        setting_window.exec()
