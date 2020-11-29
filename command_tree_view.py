from PyQt5.QtWidgets import QTreeView
from state import State


class CommandTreeView(QTreeView):

    def __init__(self, state:State):
        super().__init__()
        self.state = state
        self.setModel(self.state.command_tree_model)

