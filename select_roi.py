import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar


class SelectRoi(QWidget):

    def __init__(self, array: np.array):
        super().__init__()

        # Create the plot.
        figure, axes = plt.subplots(1, 1)
        axes.imshow(array[0, :, :], interpolation='nearest')
        figure.set_facecolor("grey")
        plot = FigureCanvas(figure)

        # Create the toolbar.
        toolbar = NavigationToolbar(plot, self)
        save_roi_button = QPushButton('Save ROI')

        # Add it to layout.
        layout = QVBoxLayout()
        layout.addWidget(plot)
        layout.addWidget(toolbar)
        layout.addWidget(save_roi_button)
        self.setLayout(layout)


