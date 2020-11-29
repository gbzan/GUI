from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QTreeView
from state import State


class FileTreeView(QTreeView):

    def __init__(self, state: State):
        super().__init__()
        self.state = state
        self.setModel(self.state.file_tree_model)
        self.clicked.connect(self.handle_click_file_tree)

    def handle_click_file_tree(self):
        self.state.command_tree_model.clear()
        self.state.command_tree_model.setHorizontalHeaderLabels(['Commands'])

        self.state.command_tree_model.invisibleRootItem().appendRow(QStandardItem('Select ROI'))


