from PyQt5.QtWidgets import QStackedWidget, QPushButton
from data import Data
from plot_map import PlotMap


class ContentWidget(QStackedWidget):

    def __init__(self, data: Data):
        super().__init__()
        self.data = data
        command_dic = {
            'Select ROI': PlotMap,
            'Show Plot': QPushButton('Soon coming'),
        }

    #def command_click(self):


