import h5py
import numpy as np
from PyQt5 import Qt
from PyQt5.QtWidgets import QPushButton, QFileDialog, QTreeWidgetItem

from data import Data
from file_tree import FileTreeWidget
from roi_treeitem import RoiTreeItem


class OpenFileButton(QPushButton):

    def __init__(self, file_tree_widget: FileTreeWidget, name: str, data: Data):
        super().__init__(name)
        self.file_tree = file_tree_widget
        self.data = data
        self.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        file_dir = QFileDialog.getOpenFileName()[0]
        if not file_dir:
            return
        file_name = file_dir.split('/')[-1]
        if not self.file_tree.findItems(file_name, Qt.Qt.MatchExactly, column=0):
            item = QTreeWidgetItem([file_name])
            self.file_tree.addTopLevelItem(item)

            # generate the datacube and save into Data class
            with h5py.File(file_dir, 'r') as f:
                datacube = np.asarray(f['/exchange/data'])
            y_len = len(datacube[0, :, 0])
            x_len = len(datacube[0, 0, :])
            self.data.datacube[file_name] = datacube
            self.data.file_dir[file_name] = file_dir
            whole_map_tree_item = RoiTreeItem(item, self.data, name='Whole Map', roi=(0, 0, x_len+1, y_len+1))
            item.addChild(whole_map_tree_item)
