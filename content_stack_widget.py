from PyQt5.QtWidgets import QStackedWidget
from data import Data
from plot_map import PlotMap
from select_roi import SelectRoi


class ContentWidget(QStackedWidget):

    def __init__(self):
        super().__init__()

    def command_click(self, data: Data, command: str):
        command_dic = {
            'Select ROI': SelectRoi,
            'Show Map': PlotMap,
            'Show Plot': PlotMap,
            'Show Average Plot': PlotMap,
        }
        if not command_dic[command]:
            print('New Command needed to be added')
            return
        key = (data.current_filename, command)
        if key not in data.content_widget_container:
            widget = command_dic[command](data.current_datacube)
            data.content_widget_container[key] = widget
            self.addWidget(widget)
        else:
            widget = data.content_widget_container[key]
        self.setCurrentWidget(widget)

