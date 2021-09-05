import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from data import Data
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar


class ShowVisMap(QWidget):
    def __init__(self, current_datacube, current_file_tree_item, data, pixel_num):
        super().__init__()

        # Create the plot.
        figure, axes = plt.subplots(1, 1)
        map_to_show = current_file_tree_item.vis_map
        x_offset, y_offset = data.current_roi[0], data.current_roi[1]
        x_len = len(data.current_datacube[0, 0, :])  
        y_len = len(data.current_datacube[0, :, 0]) 
        im = axes.imshow(map_to_show, interpolation='nearest', extent=[x_offset, x_offset+x_len-1, y_offset+y_len-1, y_offset])
        axes.set_xlabel('X-position /pixel')
        axes.set_ylabel('Y-position /pixel')
        axes.set_title('Visibility Map')
        figure.set_facecolor("#C9e8f1")
        plt.colorbar(im)
        plot = FigureCanvas(figure)

        # Create the toolbar.
        toolbar = NavigationToolbar(plot, self)

        # Add it to layout.
        layout = QVBoxLayout()
        layout.addWidget(plot)
        layout.addWidget(toolbar)
        self.setLayout(layout)
