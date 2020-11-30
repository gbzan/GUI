from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

from command_tree import CommandTreeWidget
from data import Data


class FileTreeWidget(QTreeWidget):

    def __init__(self, command_tree: CommandTreeWidget, data: Data):
        super().__init__()
        self.setHeaderLabel('Files')
        self.command_tree = command_tree
        self.clicked.connect(self.handle_click_file_tree)
        self.data = data

    def handle_click_file_tree(self):
        self.command_tree.clear()
        self.command_tree.setHeaderLabel('Commands')
        current_tree_item = self.currentItem()
        if current_tree_item.parent():
            item1 = QTreeWidgetItem(['Show Plot'])
            item2 = QTreeWidgetItem(['Show Map'])
            self.command_tree.addTopLevelItem(item1)
            self.command_tree.addTopLevelItem(item2)
            self.data.current_datacube = current_tree_item.datacube
        else:
            item1 = QTreeWidgetItem(['Select ROI'])
            self.command_tree.addTopLevelItem(item1)

