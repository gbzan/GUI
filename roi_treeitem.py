from PyQt5.QtWidgets import QTreeWidgetItem
from typing import Tuple
from data import Data


class RoiTreeItem(QTreeWidgetItem):

    def __init__(self, parent: QTreeWidgetItem, data: Data, name: str, roi: Tuple[int, int, int, int]):
        xstart, ystart, xend, yend = roi
        super().__init__([name])
        self.datacube = data.datacube[parent.text(0)][:, ystart:yend, xstart: xend]
        self.roi = roi
