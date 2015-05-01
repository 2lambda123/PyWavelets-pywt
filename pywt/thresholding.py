# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
The thresholding helper module implements the most popular signal thresholding
functions.
"""

from __future__ import division, print_function, absolute_import

import numpy as np

__all__ = ['threshold']


def threshold(data, value, mode='soft', substitute=0):
    """
    Thresholds the input data depending on the mode argument.

    In ``soft`` thresholding, the data values where their absolute value is
    less than the value param are replaced with substitute. From the data
    values with absolute value greater or equal to the thresholding value,
    a quantity of ``(signum * value)`` is subtracted.

    In ``hard`` thresholding, the data values where their absolute value is
    less than the value param are replaced with substitute. Data values with
    absolute value greater or equal to the thresholding value stay untouched.

    In ``greater`` thresholding, the data is replaced with substitute where
    data is below the thresholding value. Greater data values pass untouched.

    In ``less`` thresholding, the data is replaced with substitute where data
    is above the thresholding value. Less data values pass untouched.

    Parameters
    ----------
    data : array_like
        Numeric data.
    value : scalar
        Thresholding value.
    mode : {'soft', 'hard', 'greater', 'less'}
        Decides the type of thresholding to be applied on input data. Default
        is 'soft'.
    substitute : float, optional
        Substitute value (default: 0).

    Returns
    -------
    output : array
        Thresholded array.

    Examples
    --------
    >>> import pywt
    >>> data = np.linspace(1, 4, 7)
    >>> data
    array([ 1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> pywt.threshold(data, 2, 'soft')
    array([ 0. ,  0. ,  0. ,  0.5,  1. ,  1.5,  2. ])
    >>> pywt.threshold(data, 2, 'hard')
    array([ 0. ,  0. ,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> pywt.threshold(data, 2, 'greater')
    array([ 0. ,  0. ,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> pywt.threshold(data, 2, 'less')
    array([ 1. ,  1.5,  2. ,  0. ,  0. ,  0. ,  0. ])

    """
    data = np.asarray(data)

    if mode == 'soft':
        mvalue = -value

        cond_less = np.less(data, value)
        cond_greater = np.greater(data, mvalue)

        output = np.where(cond_less & cond_greater, substitute, data)
        output = np.where(cond_less, output + value, output)
        output = np.where(cond_greater, output - value, output)

    elif mode == 'hard':
        mvalue = -value

        cond = np.less(data, value)
        cond &= np.greater(data, mvalue)

        output = np.where(cond, substitute, data)

    elif mode == 'greater':
        output = np.where(np.less(data, value), substitute, data)

    elif mode == 'less':
        output = np.where(np.greater(data, value), substitute, data)

    else:
        raise ValueError("The mode parameter only takes value among "
                         "{'soft', 'hard', 'greater','less'}.")

    return output
