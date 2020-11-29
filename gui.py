from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QHBoxLayout, QVBoxLayout
import qdarkstyle

from command_tree_view import CommandTreeView
from file_tree_view import FileTreeView
from open_file_button_widget import OpenFileButton
from state import State


class Application(object):

    def __init__(self):
        """Initiate an Application object"""
        super().__init__()

        # set up the state object
        self.state = State()

        # Generate the widget components of the main window
        self.mainwindow = QWidget()
        self.side_bar = QWidget()
        self.content = QWidget()
        self.open_file_button = OpenFileButton(self.state, 'Open')

        # create file tree view and content tree view
        self.file_tree_view = FileTreeView(self.state)
        self.command_tree_view = CommandTreeView(self.state)

        # create and set the layout
        self.set_layout_mainwindow()
        self.set_layout_side_bar()

        # set size and style
        self.set_style()

    def set_style(self):
        self.mainwindow.resize(1024, 768)
        self.side_bar.setFixedWidth(300)

    def set_layout_mainwindow(self):
        layout_mainwindow = QHBoxLayout()
        layout_mainwindow.addWidget(self.side_bar)
        layout_mainwindow.addWidget(self.content)
        self.mainwindow.setLayout(layout_mainwindow)

    def set_layout_side_bar(self):
        layout_side_bar = QVBoxLayout()
        layout_side_bar.addWidget(self.open_file_button)
        layout_side_bar.addWidget(self.file_tree_view)
        layout_side_bar.addWidget(self.command_tree_view)
        self.side_bar.setLayout(layout_side_bar)

    def show(self):
        self.mainwindow.show()


def main():
    qapp = QApplication([])
    app = Application()
    app.show()
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    qapp.setStyleSheet(dark_stylesheet)
    qapp.exec_()


if __name__ == '__main__':
    main()
