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
        if not current_tree_item.parent():
            item1 = QTreeWidgetItem(['Select ROI'])
            self.command_tree.addTopLevelItem(item1)
            self.data.current_file_tree_item = current_tree_item
            self.data.current_datacube = self.data.datacube[current_tree_item.text(0)]
            self.data.current_filename = current_tree_item.text(0)
        elif current_tree_item.text(0) == 'Whole Map':
            item1 = QTreeWidgetItem(['Show Map'])
            item2 = QTreeWidgetItem(['Show Sine Curve'])
            self.command_tree.addTopLevelItem(item1)
            self.command_tree.addTopLevelItem(item2)
            self.data.current_filename = current_tree_item.parent_name
            self.data.current_datacube = current_tree_item.datacube
            self.data.current_roi = current_tree_item.roi
        else:
            item1 = QTreeWidgetItem(['Show Map'])
            item2 = QTreeWidgetItem(['Show Visibility Map'])
            self.command_tree.addTopLevelItem(item1)
            self.command_tree.addTopLevelItem(item2)
            self.data.current_filename = current_tree_item.parent_name
            self.data.current_datacube = current_tree_item.datacube
            self.data.current_roi = current_tree_item.roi
