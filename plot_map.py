from PIL.Image import EXTENT
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
import matplotlib.pyplot as plt
from data import Data
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar


class PlotMap(QWidget):

    def __init__(self, array: np.array, file_tree, data: Data):
        super().__init__()
        x_offset, y_offset = data.current_roi[0], data.current_roi[1]
        x_len = len(data.current_datacube[0, 0, :])  
        y_len = len(data.current_datacube[0, :, 0])  
        # Create the plot.
        figure, axes = plt.subplots(1, 1)
        axes.imshow(array[0, :, :], interpolation='nearest', extent=[x_offset, x_offset+x_len-1, y_offset+y_len-1, y_offset])
        axes.set_xlabel('X-position /pixel')
        axes.set_ylabel('Y-position /pixel')
        axes.set_title('Intensity Map')
        figure.set_facecolor("#C9e8f1")
        plot = FigureCanvas(figure)

        # Create the toolbar.
        toolbar = NavigationToolbar(plot, self)

        # Add it to layout.
        layout = QVBoxLayout()
        layout.addWidget(plot)
        layout.addWidget(toolbar)
        self.setLayout(layout)
