from PyQt5.QtWidgets import QTreeWidgetItem, QWidget, QTreeWidget, QInputDialog

from content_stack_widget import ContentWidget
from data import Data
import calcualte_visibility as cal_vis


class CommandTreeWidget(QTreeWidget):

    def __init__(self, data: Data):
        super().__init__()
        self.setHeaderLabel('Commands')
        self.clicked.connect(self.handle_command_tree_click)
        self.data = data

    def handle_command_tree_click(self):
        current_tree_item = self.currentItem()
        command = self.currentItem().text(0)
        pixel_num = 5
        #=======This block or code is saved for potential use of a pop-up window to select pixel_number
        # if command == 'Show Sine Curve':
        #     selections = ['5', '10', '15', '20']
        #     box = QInputDialog()
        #     item, ok = box.getItem(self, 'Input pixel number', 'Select pixel number',selections, 0)
        #     if ok:
        #         pixel_num = int(item)
        #     else:
        #         pixel_num = 5
        if command == 'Calculate Visibility':
            if current_tree_item.childCount():
                return
            item1 = QTreeWidgetItem(['Show Visibility Map'])
            item2 = QTreeWidgetItem(['Show Visibility Distribution'])
            current_tree_item.addChild(item1)
            current_tree_item.addChild(item2)
            current_tree_item.setExpanded(True)
            self.data.current_file_tree_item.vis_map = cal_vis.get_vis_map(self.data)
            return
        self.data.only_content_widget.command_click(self.data, command, pixel_num)
