import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QInputDialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import RectangleSelector
from data import Data
from roi_treeitem import RoiTreeItem


class SelectRoi(QWidget):

    def __init__(self, array: np.array, file_tree, data: Data):
        super().__init__()

        self.current_tree = file_tree
        self.data = data
        self.array = array
        self.selected_pixels = None
        # Create the plot.
        figure, axes = plt.subplots(1, 1)
        axes.imshow(array[0, :, :], interpolation='nearest')
        figure.set_facecolor("grey")
        figure.canvas.mpl_connect('rectangle_select_event', self.anything)
        self.anything.RS = RectangleSelector(
            axes, self.rectangle_select_callback,
            drawtype='box', useblit=True,
            button=[1, 3],  # don't use middle button
            minspanx=5, minspany=5,
            spancoords='pixels',
            interactive=True,
            rectprops=dict(facecolor='white', edgecolor='black', linewidth=5, alpha=0.2, fill=True),
        )

        # Create the toolbar.
        toolbar = NavigationToolbar(figure.canvas, self)
        save_roi_button = QPushButton('Save ROI')

        # Add it to layout.
        layout = QVBoxLayout()
        layout.addWidget(figure.canvas)
        layout.addWidget(toolbar)
        layout.addWidget(save_roi_button)
        self.setLayout(layout)

        # set up save button function
        save_roi_button.clicked.connect(self.handle_save_roi_button)

    def rectangle_select_callback(self, eclick, erelease):
        x1, y1 = int(round(eclick.xdata)), int(round(eclick.ydata))
        x2, y2 = int(round(erelease.xdata)), int(round(erelease.ydata))
        self.selected_pixels = (x1, y1, x2, y2)
        print(self.selected_pixels)

    def handle_save_roi_button(self):
        parent = self.current_tree
        box = QInputDialog()
        box.resize(500, 500)
        box.setLabelText('Enter ROI name:')
        box.setInputMode(QInputDialog.TextInput)
        ok = box.exec_()
        roi_name = box.textValue()
        if ok:
            parent.addChild(RoiTreeItem(parent, self.data, roi_name, self.selected_pixels))

    @staticmethod
    def anything(event):
        pass

