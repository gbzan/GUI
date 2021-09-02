from PyQt5.QtWidgets import QWidget, QTreeWidget, QInputDialog

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
        pixel_num = 0
        if command == 'Show Sine Curve':
            selections = ['5', '10', '15', '20']
            box = QInputDialog()
            # box.resize(800, 100)
            item, ok = box.getItem(self, 'Input pixel number', 'Select pixel number',selections, 0)
            if ok:
                pixel_num = int(item)
            else:
                pixel_num = 5
        self.data.only_content_widget.command_click(self.data, command, pixel_num)
