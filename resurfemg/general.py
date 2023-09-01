"""
Copyright 2022 Netherlands eScience Center and University of Twente
Licensed under the Apache License, version 2.0. See LICENSE for details.

This file contains multi-purpose functions used throughout the
library.
"""

from collections import namedtuple

class Range(namedtuple('RangeBase', 'start,end')):

    """Utility class for working with ranges (intervals).

    :ivar start: Start of the range
    :type start: ~number.Number
    :ivar end: End of the range
    :type end: ~number.Number

    """

    def intersects(self, other):
        """Returns :code:`True` if this range intersects :code:`other` range.

        :param other: Another range to compare this one to
        :type other: ~resurfemg.helper_functions.Range

        :returns: :code:`True` if this range intersects another range
        :rtype: bool
        """
        return (
            (self.end >= other.end) and (self.start < other.end) or
            (self.end >= other.start) and (self.start < other.start) or
            (self.end < other.end) and (self.start >= other.start)
        )

    def precedes(self, other):
        """Returns :code:`True` if this range precedes :code:`other` range.

        :param other: Another range to compare this one to
        :type other: ~resurfemg.helper_functions.Range

        :returns: :code:`True` if this range strictly precedes another
            range
        :rtype: bool
        """
        return self.end < other.start

    def to_slice(self):
        """Converts this range to a :class:`slice`.

        :returns: A slice with its start set to this range's start and
            end set to this range's end
        :rtype: slice
        """
        return slice(*map(int, self))   # maps whole tuple set

def zero_one_for_jumps_base(array, cut_off):
    """This function takes an array and makes it binary (0, 1) based
    on a cut-off value.

    :param array: An array
    :type array: ~numpy.ndarray
    :param cut_off: The number defining a cut-off line for binarization
    :type cut_off: float

    :returns: Binarized list that can be turned into array
    :rtype: list
    """
    array_list = []
    for i in array:
        if i < cut_off:
            i = 0
        else:
            i = 1
        array_list.append(i)
    return array_list