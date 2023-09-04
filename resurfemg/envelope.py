"""
Copyright 2022 Netherlands eScience Center and University of Twente
Licensed under the Apache License, version 2.0. See LICENSE for details.

This file contains functions extract the envelopes from EMG arrays.
"""

import numpy as np

def full_rolling_rms(x, N):
    """This function computes a root mean squared envelope over an
    array :code:`x`.  To do this it uses number of sample values
    :code:`N`. It differs from :func:`naive_rolling_rms` by that the
    output is the same length as the input vector.

    :param x: Samples from the EMG
    :type x: ~numpy.ndarray
    :param N: Length of the sample use as window for function
    :type N: int

    :returns: The root-mean-squared EMG sample data
    :rtype: ~numpy.ndarray
    """
    x_pad = np.pad(x, (0, N-1), 'constant', constant_values=(0, 0))
    x2 = np.power(x_pad, 2)
    window = np.ones(N)/float(N)
    emg_rms = np.sqrt(np.convolve(x2, window, 'valid'))
    return emg_rms

def naive_rolling_rms(x, N):
    """This function computes a root mean squared envelope over an
    array :code:`x`. To do this it uses number of sample values
    :code:`N`.

    :param x: Samples from the EMG
    :type x: ~numpy.ndarray
    :param N: Length of the sample use as window for function
    :type N: int

    :returns: The root-mean-squared EMG sample data
    :rtype: ~numpy.ndarray
    """
    xc = np.cumsum(abs(x)**2)
    emg_rms = np.sqrt((xc[N:] - xc[:-N])/N)
    return emg_rms

def running_smoother(array):
    """
    This is the smoother to use in time calculations
    """
    n = len(array) // 10
    new_list = np.convolve(abs(array), np.ones(n), "valid") / n
    zeros = np.zeros(n - 1)
    smoothed_array = np.hstack((new_list, zeros))
    return smoothed_array

def smooth_for_baseline(
    single_filtered_array, start=None, end=None, smooth=100
):
    """
    This is an adaptive smoothing a series that overvalues closer numbers.

    :param single_filtered_array: Array.
    :type single_filtered_array: ~numpy.ndarray
    :param start: The number of samples to work from
    :type start: int
    :param end: The number of samples to work until
    :type end: int
    :param smooth: The number of samples to work over
    :type smooth: int

    :return: tuple of arrays
    :rtype: tuple
    """
    array = single_filtered_array[start:end]
    dists = np.zeros(len(array))
    wmax, wmin = 0, 0
    nwmax, nwmin = 0, 0
    tail = (smooth - 1) / smooth

    for i, elt in enumerate(array[1:]):
        if elt > 0:
            nwmax = wmax * tail + elt / smooth
        else:
            nwmin = wmin * tail + elt / smooth
        dist = nwmax - nwmin
        dists[i] = dist
        wmax, wmin = nwmax, nwmin
    return array, dists

def smooth_for_baseline_with_overlay(
    my_own_array, threshold=10, start=None, end=None, smooth=100
):
    """This is the same as smooth for baseline, but we also get an
    overlay 0 or 1 mask tagging the baseline.

    :param my_own_array: Array
    :type  my_own_array: ~numpy.ndarray
    :param threshold: Number where to cut the mask for overlay
    :type threshold: int
    :param start: The number of samples to work from
    :type start: int
    :param end: The number of samples to work until
    :type end: int
    :param smooth: The number of samples to work over
    :type smooth: int

    :return: tuple of arrays
    :rtype: tuple
    """
    array = my_own_array[start:end]
    overlay = np.zeros(len(array)).astype('int8')
    dists = np.zeros(len(array))
    wmax, wmin = 0, 0
    nwmax, nwmin = 0, 0
    count, filler = 0, False
    tail = (smooth - 1) / smooth
    switched = 0

    for i, elt in enumerate(array[1:]):
        if elt > 0:
            nwmax = wmax * tail + elt / smooth
        else:
            nwmin = wmin * tail + elt / smooth
        dist = nwmax - nwmin
        if (i > smooth) and (i - switched > smooth):
            vodist = dists[i - smooth]
            if (vodist / dist > threshold) or (dist / vodist > threshold):
                filler = not filler
                # Now we need to go back and repaing the values in the overlay
                # because the change was detected after `smooth' interval
                overlay[i - smooth:i] = filler
                count += 1
                switched = i
        overlay[i] = filler
        dists[i] = dist
        wmax, wmin = nwmax, nwmin
    return array, overlay, dists

def vect_naive_rolling_rms(x, N):
    """This function computes a root mean squared envelope over an
    array :code:`x`.  To do this it uses number of sample values
    :code:`N`. It differs from :func:`naive_rolling_rms` by the way
    the signal is put in.

    :param xc: Samples from the EMG
    :type xc: ~numpy.ndarray

    :param N: Legnth of the sample use as window for function
    :type N: int

    :return: The root-mean-squared EMG sample data
    :rtype: ~numpy.ndarray
    """
    xc = np.cumsum(np.abs(x)**2)
    emg_rms = np.sqrt((xc[N:] - xc[:-N])/N)
    return emg_rms

