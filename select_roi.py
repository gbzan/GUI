import numpy as np
from PyQt5.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QInputDialog, QLabel, QSlider
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import RectangleSelector
from data import Data
from roi_treeitem import RoiTreeItem
from PyQt5.QtCore import Qt


class SelectRoi(QWidget):

    def __init__(self, array: np.array, file_tree, data: Data):
        super().__init__()

        self.current_tree = file_tree
        self.data = data
        self.array = array
        self.selected_pixels = None

        # Create the intensity plot.
        figure, self.axes = plt.subplots(1, 1, constrained_layout=True)
        self.axes.imshow(self.array[0, :, :], interpolation='nearest')
        self.set_map_axes(self.axes)
        figure.set_facecolor("#C9e8f1")
        self.map_canvas = FigureCanvas(figure)
        figure.canvas.mpl_connect('rectangle_select_event', self.anything)
        self.anything.RS = RectangleSelector(
            self.axes, self.rectangle_select_callback,
            drawtype='box', useblit=True,
            button=[1, 3],  # don't use middle button
            minspanx=5, minspany=5,
            spancoords='pixels',
            interactive=True,
            rectprops=dict(facecolor='white', edgecolor='black', linewidth=5, alpha=0.2, fill=True),
        )

        # Create the intensity histogram plot
        fig, self.ax = plt.subplots(1,1,constrained_layout=True)
        default_hist_data = self.array[0, :, :].flatten()
        self.ax.hist(default_hist_data, bins=100, orientation='horizontal')
        self.set_histogram_axes(self.ax)
        self.histogram_plot = FigureCanvas(fig)
        self.histogram_plot.setMaximumWidth(60)
        self.histogram_plot.setMinimumWidth(30)

        # Create the step_slider + label widget
        self.step_slider_label_widget = QWidget()
        self.step_slider_label_widget.setFixedHeight(40)
        self.step_label_widget = QLabel('step-0')
        self.step_slider = QSlider(Qt.Horizontal)
        self.set_slider_style(self.step_slider, 0, len(self.array)-1, QSlider.TicksAbove, 1, 1, self.step_slider_update)
        self.set_step_slider_label_layout(self.step_slider_label_widget, self.step_slider, self.step_label_widget)

        # Create histogram slider + Labels Widgets
        min_histogram_label_widget = QWidget()
        min_histogram_label_widget.setMaximumWidth(50)
        max_histogram_label_widget = QWidget()
        max_histogram_label_widget.setMaximumWidth(65)
        self.min_slider = QSlider(Qt.Vertical)
        self.set_slider_style(
            self.min_slider,
            min(default_hist_data),
            max(default_hist_data),
            QSlider.TicksRight,
            100,
            10,
            self.min_histogram_slider_update)
        self.max_slider = QSlider(Qt.Vertical)
        self.set_slider_style(
            self.max_slider,
            min(default_hist_data),
            max(default_hist_data),
            QSlider.TicksLeft,
            100,
            10,
            self.max_histogram_slider_update)
        self.min_label_widget = QLabel()
        self.min_label_widget.setText('MIN<br>' + str(min(self.array[0, :, :].flatten())))
        self.min_label_widget.setMinimumWidth(50)
        self.max_label_widget = QLabel()
        self.max_label_widget.setText('MAX<br>' + str(max(self.array[0, :, :].flatten())))
        self.max_label_widget.setMinimumWidth(65)
        self.max_slider.setValue(max(default_hist_data))
        self.set_min_hist_label_layout(min_histogram_label_widget, self.min_slider, self.min_label_widget)
        self.set_max_hist_label_layout(max_histogram_label_widget, self.max_slider, self.max_label_widget)
        
        # Create the toolbar and save_button.
        toolbar = NavigationToolbar(figure.canvas, self)
        save_roi_button = QPushButton('Save ROI')
        save_roi_button.clicked.connect(self.handle_save_roi_button)

        # Add all into the layout.
        self.left_box_widget = QWidget()
        self.set_left_box_layout(self.left_box_widget, self.map_canvas, self.step_slider_label_widget, toolbar, save_roi_button)
        self.right_box_widget = QWidget()
        self.set_right_box_layout(self.right_box_widget, self.histogram_plot, min_histogram_label_widget, max_histogram_label_widget)
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_box_widget)
        main_layout.addWidget(self.right_box_widget)
        self.setLayout(main_layout)

    def set_right_box_layout(self, whole_widget, plot_widget, slider_label1, slider_label2):
        layout = QHBoxLayout()
        layout.addWidget(slider_label1)
        layout.addWidget(plot_widget)
        layout.addWidget(slider_label2)
        whole_widget.setLayout(layout)
    
    def set_left_box_layout(self, whole_widget, plot_widget, slider_label, toolbar, button):
        layout = QVBoxLayout()
        layout.addWidget(plot_widget)
        layout.addWidget(slider_label)
        layout.addWidget(toolbar)
        layout.addWidget(button)
        whole_widget.setLayout(layout)

    def set_max_hist_label_layout(self, whole_widget, slider, label):
        whole_layout = QVBoxLayout()
        whole_layout.addWidget(label)
        whole_layout.addWidget(slider)
        whole_widget.setLayout(whole_layout)

    def set_min_hist_label_layout(self, whole_widget, slider, label):
        whole_layout = QVBoxLayout()
        whole_layout.addWidget(slider)
        whole_layout.addWidget(label)
        whole_widget.setLayout(whole_layout)

    def set_step_slider_label_layout(self, whole_widget, slider, label):
        whole_layout = QHBoxLayout()
        whole_layout.addWidget(slider)
        whole_layout.addWidget(label)
        whole_widget.setLayout(whole_layout)

    def set_slider_style(self, slider, min_val, max_val, tick_position, tick_interval, tick_step, click_func):
        slider.setMinimumWidth(20)
        slider.setRange(min_val, max_val)
        slider.setTickPosition(tick_position)
        slider.setTickInterval(tick_interval)
        slider.setSingleStep(tick_step)
        slider.valueChanged.connect(click_func)     

    def set_map_axes(self, ax):
        ax.set_xlabel('X-position /pixel')
        ax.set_ylabel('Y-position /pixel')
        ax.set_title('Intensity Map')
    
    def set_histogram_axes(self, ax):
        ax.xaxis.set_ticks([])
        ax.tick_params(axis='y', labelrotation=270, labelsize=6)

    def step_slider_update(self, val):
        new_image = self.array[val, :, :]
        self.step_label_widget.setText('step-'+str(val))
        self.min_label_widget.setText('MIN<br>' + str(min(new_image.flatten())))
        self.min_slider.setRange(min(new_image.flatten()), max(new_image.flatten()))
        self.max_label_widget.setText('MAX<br>' + str(max(new_image.flatten())))
        self.max_slider.setRange(min(new_image.flatten()), max(new_image.flatten()))
        self.max_slider.setValue(max(new_image.flatten()))
        self.axes.cla()
        self.ax.cla()
        self.axes.imshow(new_image, interpolation='nearest')
        self.set_map_axes(self.axes)
        self.ax.hist(new_image.flatten(), bins=100, orientation='horizontal')
        self.set_histogram_axes(self.ax)
        self.histogram_plot.draw()
        self.map_canvas.draw()

    def min_histogram_slider_update(self, val):
        self.min_label_widget.setText('MIN<br>' + str(val))
        self.histogram_slider_udpate()

    def max_histogram_slider_update(self, val):
        self.max_label_widget.setText('MAX<br>' + str(val))
        self.histogram_slider_udpate()

    def histogram_slider_udpate(self):
        self.axes.cla()
        self.ax.cla()
        step_num = int(self.step_label_widget.text()[5:])
        current_image = self.array[step_num, :, :]
        min_count, max_count = int(self.min_label_widget.text()[7:]), int(self.max_label_widget.text()[7:])
        self.axes.imshow(
            current_image, 
            interpolation='nearest', 
            vmin=min_count,
            vmax= max_count
            )
        self.set_map_axes(self.axes)
        self.ax.hist(current_image.flatten(), range=(min_count,max_count), bins=100, orientation='horizontal')
        self.set_histogram_axes(self.ax)
        self.map_canvas.draw()
        self.histogram_plot.draw()

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
            if roi_name in self.data.roi_names:
                QMessageBox.critical(box, 'Error','Name existed! Please give it an unique name.')
            else:
                parent.addChild(RoiTreeItem(parent, self.data, roi_name, self.selected_pixels))
                self.data.roi_names.add(roi_name)

    @staticmethod
    def anything(event):
        pass
