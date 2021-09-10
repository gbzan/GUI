from PIL.Image import EXTENT
import numpy as np
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget, QVBoxLayout, QPushButton
import matplotlib.pyplot as plt
from data import Data
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import Qt


class PlotMap(QWidget):

    def __init__(self, array: np.array, file_tree, data: Data):
        super().__init__()
        x_offset, y_offset = data.current_roi[0], data.current_roi[1]
        x_len = len(data.current_datacube[0, 0, :])  
        y_len = len(data.current_datacube[0, :, 0])  
        z_len = len(data.current_datacube[:, 0, 0])  
        # Create the plot.
        figure, axes = plt.subplots(1, 1)
        axes.imshow(array[0, :, :], interpolation='nearest', extent=[x_offset, x_offset+x_len-1, y_offset+y_len-1, y_offset])
        axes.set_xlabel('X-position /pixel')
        axes.set_ylabel('Y-position /pixel')
        axes.set_title('Intensity Map')
        figure.set_facecolor("#C9e8f1")
        plot = FigureCanvas(figure)

        # Create Slider Widget
        slider_widget = QWidget()
        slider_widget.setFixedHeight(40)
        label_widget = QLabel('0')
        
        step_slider = QSlider(Qt.Horizontal)
        step_slider.setRange(0, z_len-1)
        step_slider.setFocusPolicy(Qt.StrongFocus)
        step_slider.setTickPosition(QSlider.TicksAbove)
        step_slider.setTickInterval(1)
        step_slider.setSingleStep(1)


        def slider_update(val):
            label_widget.setText(str(val))
            axes.cla()
            axes.imshow(array[val, :, :], interpolation='nearest', extent=[x_offset, x_offset+x_len-1, y_offset+y_len-1, y_offset])
            plot.draw()
        step_slider.valueChanged.connect(slider_update)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(step_slider)
        slider_layout.addWidget(label_widget)
        slider_widget.setLayout(slider_layout)

        # Create the toolbar.
        toolbar = NavigationToolbar(plot, self)

        # Add it to layout.
        layout = QVBoxLayout()
        layout.addWidget(plot)
        layout.addWidget(toolbar)
        layout.addWidget(slider_widget)
        self.setLayout(layout)

        
            
    
