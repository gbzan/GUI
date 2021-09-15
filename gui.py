import qdarkstyle
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from command_tree import CommandTreeWidget
from content_stack_widget import ContentWidget
from data import Data
from file_tree import FileTreeWidget
from open_file_button_widget import OpenFileButton
from setting_button import SettingButton


class Application(object):

    def __init__(self):
        """Initiate an Application object"""
        super().__init__()

        self.data = Data()
        # set up the file tree and command tree widget
        self.command_tree_widget = CommandTreeWidget(self.data)
        self.file_tree_widget = FileTreeWidget(self.command_tree_widget, self.data)

        # Generate the widget components of the main window
        self.mainwindow = QWidget()
        self.side_bar = QWidget()
        self.content = ContentWidget()
        self.data.only_content_widget = self.content
        self.buttons = QWidget()
        self.open_file_button = OpenFileButton(self.file_tree_widget, 'Open File', self.data)
        self.setting_button = SettingButton('Settings', self.data)

        # create and set the layout
        self.set_layout_mainwindow()
        self.set_layout_side_bar()
        self.set_layout_buttons()
        # set size and style
        self.set_style()

    def set_style(self):
        self.mainwindow.resize(1400, 768)
        self.side_bar.setFixedWidth(320)

    def set_layout_mainwindow(self):
        layout_mainwindow = QHBoxLayout()
        layout_mainwindow.addWidget(self.side_bar)
        layout_mainwindow.addWidget(self.content)
        self.mainwindow.setLayout(layout_mainwindow)

    def set_layout_side_bar(self):
        layout_side_bar = QVBoxLayout()
        layout_side_bar.addWidget(self.buttons)
        layout_side_bar.addWidget(self.file_tree_widget)
        layout_side_bar.addWidget(self.command_tree_widget)
        self.side_bar.setLayout(layout_side_bar)

    def set_layout_buttons(self):
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.open_file_button)
        layout_buttons.addWidget(self.setting_button)
        self.buttons.setLayout(layout_buttons)

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
