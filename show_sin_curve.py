import numpy as np
import scipy.optimize
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
        # get original data scatter
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
        
        # get the fitting of raw data (refer 'PS_VisibilityMap_mp.py')
        def fit_sin(tt, yy):
            '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
            tt = np.array(range(z_len))
            yy = np.array(result)
            ff = np.fft.fftfreq(len(tt), (tt[1] - tt[0]))  # assume uniform spacing
            Fyy = abs(np.fft.fft(yy))
            guess_freq = abs(ff[np.argmax(Fyy[1:]) + 1])  # excluding the zero frequency "peak", which is related to offset
            guess_amp = np.std(yy) * 2. ** 0.5
            guess_offset = np.mean(yy)
            guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset])

            def sinfunc(t, A, w, p, c):  return A * np.sin(w * t + p) + c

            popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess, maxfev=100)
            return popt

        # Plot two sets of data in one figure
        figure, axes = plt.subplots(1, 1)
        axes.scatter(range(z_len), result, label='Stepping point', color='red')
        x_dimension = np.linspace(0, z_len, 100)
        A, w, p, c = fit_sin(range(z_len), result)
        fitfunc = lambda t: A * np.sin(w * t + p) + c
        FitPSCurve = fitfunc(x_dimension)
        darkcount = self.data.darkcount
        visibility = ((np.max(FitPSCurve) - darkcount) - (np.min(FitPSCurve) - darkcount)) / (
            (np.max(FitPSCurve) - darkcount) + (np.min(FitPSCurve) - darkcount))
        axes.plot(x_dimension, fitfunc(x_dimension), label='Fitting phase stepping curve')
        axes.set_xlabel('steppings')
        axes.set_ylabel('counts')
        axes.legend(shadow=True)
        axes.set_title(f'(center {2*self.pixel_num} pixels) Fitted Visibility={100*visibility:.2f}%')

        plot_canvas = FigureCanvas(figure)

        # Create the toolbar.
        toolbar = NavigationToolbar(plot_canvas, self)

        # Add it to layout.
        layout = QVBoxLayout()
        layout.addWidget(plot_canvas)
        layout.addWidget(toolbar)
        self.setLayout(layout)
