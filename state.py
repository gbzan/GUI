from PyQt5.QtGui import QStandardItemModel


class State(object):

    def __init__(self):
        self.dir_dic = {}
        self.current_dir = None

        self.file_tree_model = QStandardItemModel()
        self.file_tree_model.setHorizontalHeaderLabels(['Files'])

        self.command_tree_model = QStandardItemModel()
        self.command_tree_model.setHorizontalHeaderLabels(['Commands'])



