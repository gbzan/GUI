from data import Data
from PyQt5.QtWidgets import QPushButton, QInputDialog


class SettingButton(QPushButton):

    def __init__(self, name: str, data: Data):
        super().__init__(name)
        self.data = data
        self.clicked.connect(self.handle_click_setting_button)
    
    def handle_click_setting_button(self):
        text, ok = QInputDialog().getText(self, "Input Darkcounts",
                                     "Darkcounts:")
        if ok and text:
            self.data.darkcount = int(text)
            print(self.data.darkcount)
        else:
            print("didn't change")
