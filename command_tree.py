from PyQt5.QtWidgets import QTreeWidget
from data import Data
from plot_map import PlotMap


class CommandTreeWidget(QTreeWidget):

    def __init__(self, data: Data):
        super().__init__()
        self.setHeaderLabel('Commands')
        self.clicked.connect(self.handle_command_tree_click)
        self.data = data

    def handle_command_tree_click(self):
        current_item = self.currentItem()
        if current_item.text(0) == 'Show Plot':
            widget = PlotMap(self.data.current_datacube)




