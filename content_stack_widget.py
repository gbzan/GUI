from PyQt5.QtWidgets import QStackedWidget
from data import Data
from plot_map import PlotMap
from select_roi import SelectRoi
from show_sin_curve import ShowSinCurve


class ContentWidget(QStackedWidget):

    def __init__(self):
        super().__init__()

    def command_click(self, data: Data, command: str, pixel_num):
        command_dic = {
            'Select ROI': SelectRoi,
            'Show Map': PlotMap,
            'Show Sine Curve': ShowSinCurve,
            'Show Visibility Map': PlotMap,
        }
        key = (data.current_roi, command, pixel_num)
        if key not in data.content_widget_container:
            widget = command_dic[command](data.current_datacube, data.current_file_tree_item, data, pixel_num)
            data.content_widget_container[key] = widget
            self.addWidget(widget)
        else:
            widget = data.content_widget_container[key]
        self.setCurrentWidget(widget)
