import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

class ShowSinCurve(QWidget):
    
    def __init__(self, array: np.array, file_tree, data, pixel_num):
        super().__init__()
        
        self.pixel_num = pixel_num
        self.data = data
        self.create_sin_curve()
    
    def create_sin_curve(self):
        datacube = self.data.current_datacube
        y_len = len(datacube[0, :, 0])
        x_len = len(datacube[0, 0, :])
        z_len = len(datacube[:, 0, 0])
        y_start = y_len // 2 - self.pixel_num
        y_end = y_len // 2 + self.pixel_num
        x_start = x_len // 2 - self.pixel_num
        x_end = x_len // 2 + self.pixel_num
        result = []
        for i in range(z_len):
            intensity = 0
            for j in range(y_start, y_end):
                for k in range(x_start, x_end):
                    intensity += datacube[i, j, k]
            result.append(intensity)
        figure, axes = plt.subplots(1, 1)
        axes.scatter(range(z_len), result)
        axes.set_xlabel('frame')
        axes.set_ylabel('counts')
        axes.set_title('Sine Curve Fitting')

        plot = FigureCanvas(figure)

        # Create the toolbar.
        toolbar = NavigationToolbar(plot, self)

        # Add it to layout.
        layout = QVBoxLayout()
        layout.addWidget(plot)
        layout.addWidget(toolbar)
        self.setLayout(layout)
