"""
Copyright 2022 Netherlands eScience Center and University of Twente
Licensed under the Apache License, version 2.0. See LICENSE for details.

This file contains functions extract the envelopes from EMG arrays.
"""


import numpy as np

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

