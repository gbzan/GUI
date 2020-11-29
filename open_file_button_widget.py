from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QPushButton, QFileDialog
from state import State


class OpenFileButton(QPushButton):

    def __init__(self, state: State, name: str):
        super().__init__(name)
        self.state = state
        self.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        file_dir = QFileDialog.getOpenFileName()[0]
        if not file_dir:
            return
        file_name = file_dir.split('/')[-1]
        if not self.state.file_tree_model.findItems(file_name):
            item = QStandardItem(file_name)
            self.state.file_tree_model.invisibleRootItem().appendRow(item)





