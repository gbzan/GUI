import numpy as np
import scipy.optimize
import multiprocessing as mp
from data import Data


def get_visibility_from_one_pixel(datacube, y, x, darkcount):
    counts_from_all_steps = []
    steps = len(datacube[:,0,0])
    for i in range(steps):
        counts_from_all_steps.append(datacube[i,y,x])
    fitfunc = fit_sin(range(steps), counts_from_all_steps)
    x_dimension = np.linspace(0, steps, 100)
    fitted_val = fitfunc(x_dimension)
    visibility = ((np.max(fitted_val) - darkcount) - (np.min(fitted_val) - darkcount)) / (
            (np.max(fitted_val) - darkcount) + (np.min(fitted_val) - darkcount))
    return y, x, visibility

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1] - tt[0]))  # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:]) + 1])  # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2. ** 0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.sin(w * t + p) + c

    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess, maxfev=10000)
    A, w, p, c = popt
    f = w / (2. * np.pi)
    fitfunc = lambda t: A * np.sin(w * t + p) + c
    return fitfunc

def get_vis_map(data: Data):
    datacube = data.current_datacube
    y_len = len(datacube[0, :, 0])
    x_len = len(datacube[0, 0, :])
    all_points = []
    for i in range(y_len):
        for j in range(x_len):
            all_points.append((i, j))
    with mp.Pool(processes=data.core_num) as pool:
        result = pool.starmap(get_visibility_from_one_pixel, [(datacube, *point, data.darkcount) for point in all_points])
    vis_map = np.zeros((y_len, x_len))
    for element in result:
        y, x, visibility = element
        vis_map[y, x] = visibility
    return vis_map
