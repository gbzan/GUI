from PyQt5.QtWidgets import QTreeWidget

from content_stack_widget import ContentWidget
from data import Data
from plot_map import PlotMap


class CommandTreeWidget(QTreeWidget):

    def __init__(self, data: Data):
        super().__init__()
        self.setHeaderLabel('Commands')
        self.clicked.connect(self.handle_command_tree_click)
        self.data = data

    def handle_command_tree_click(self):
        command = self.currentItem().text(0)
        self.data.only_content_widget.command_click(self.data, command)




