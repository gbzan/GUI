from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from data import Data
import numpy as np
from lmfit.models import GaussianModel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

class ShowVisDistribution(QWidget):
    def __init__(self, current_datacube, current_file_tree_item, data):
        super().__init__()
        all_visibility = current_file_tree_item.vis_map.flatten()
        smallest_vis, biggest_vis = np.ndarray.min(all_visibility), np.ndarray.max(all_visibility)
        figure, axes = plt.subplots(1, 1)
        weight = all_visibility.copy() / len(all_visibility)
        vals, bins, patches, = axes.hist(all_visibility, bins=100, weights=weight)
        axes.set_xlabel('Visibility')
        axes.set_ylabel('Probability')
        # Gaussian Fitting
        x0 = np.linspace(smallest_vis, biggest_vis, 100)
        mod = GaussianModel()
        pars = mod.guess(vals, x=x0)
        out = mod.fit(vals, pars, x=x0)
        axes.plot(x0, out.best_fit, color='red')
        mu, sigma = out.params['center'].value, out.params['sigma'].value
        
        axes.set_title(f'Histogram of Visibility (mu={mu:.2f}, sigma={sigma:.2f})')
        plot = FigureCanvas(figure)
        
        # Create the toolbar.
        toolbar = NavigationToolbar(plot, self)

        # Add it to layout.
        layout = QVBoxLayout()
        layout.addWidget(plot)
        layout.addWidget(toolbar)
        self.setLayout(layout)
