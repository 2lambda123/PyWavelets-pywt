# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
2D Discrete Wavelet Transform and Inverse Discrete Wavelet Transform.
"""

from __future__ import division, print_function, absolute_import

__all__ = ['dwt2', 'idwt2', 'swt2', 'dwtn', 'idwtn']

from itertools import cycle, product

import numpy as np

from ._extensions._pywt import Wavelet, Modes
from ._extensions._dwt import dwt_axis, idwt_axis
from ._swt import swt


def dwt2(data, wavelet, mode='symmetric'):
    """
    2D Discrete Wavelet Transform.

    Parameters
    ----------
    data : ndarray
        2D array with input data
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see Modes (default: 'symmetric')

    Returns
    -------
    (cA, (cH, cV, cD)) : tuple
        Approximation, horizontal detail, vertical detail and diagonal
        detail coefficients respectively.  Horizontal refers to array axis 0.

    Examples
    --------
    >>> import pywt
    >>> data = np.ones((4,4), dtype=np.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> cA, (cH, cV, cD) = coeffs
    >>> cA
    array([[ 2.,  2.],
           [ 2.,  2.]])
    >>> cV
    array([[ 0.,  0.],
           [ 0.,  0.]])

    """
    data = np.asarray(data)
    if data.ndim != 2:
        raise ValueError("Expected 2-D data array")

    coefs = dwtn(data, wavelet, mode)
    return coefs['aa'], (coefs['da'], coefs['ad'], coefs['dd'])


def idwt2(coeffs, wavelet, mode='symmetric'):
    """
    2-D Inverse Discrete Wavelet Transform.

    Reconstructs data from coefficient arrays.

    Parameters
    ----------
    coeffs : tuple
        (cA, (cH, cV, cD)) A tuple with approximation coefficients and three
        details coefficients 2D arrays like from `dwt2()`
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see Modes (default: 'symmetric')

    Examples
    --------
    >>> import pywt
    >>> data = np.array([[1,2], [3,4]], dtype=np.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> pywt.idwt2(coeffs, 'haar')
    array([[ 1.,  2.],
           [ 3.,  4.]])

    """
    # L -low-pass data, H - high-pass data
    LL, (HL, LH, HH) = coeffs
    if not all(c.ndim == 2 for c in (LL, HL, LH, HL) if c is not None):
        raise TypeError("All input coefficients arrays must be 2D.")

    coeffs = {'aa': LL, 'da': HL, 'ad': LH, 'dd': HH}
    return idwtn(coeffs, wavelet, mode)


def dwtn(data, wavelet, mode='symmetric'):
    """
    Single-level n-dimensional Discrete Wavelet Transform.

    Parameters
    ----------
    data : ndarray
        n-dimensional array with input data.
    wavelet : Wavelet object or name string
        Wavelet to use.
    mode : str, optional
        Signal extension mode, see `Modes`.  Default is 'symmetric'.

    Returns
    -------
    coeffs : dict
        Results are arranged in a dictionary, where key specifies
        the transform type on each dimension and value is a n-dimensional
        coefficients array.

        For example, for a 2D case the result will look something like this::

            {'aa': <coeffs>  # A(LL) - approx. on 1st dim, approx. on 2nd dim
             'ad': <coeffs>  # V(LH) - approx. on 1st dim, det. on 2nd dim
             'da': <coeffs>  # H(HL) - det. on 1st dim, approx. on 2nd dim
             'dd': <coeffs>  # D(HH) - det. on 1st dim, det. on 2nd dim
            }

    """
    data = np.asarray(data)
    if np.iscomplexobj(data):
        keys = (''.join(k) for k in product('ad', repeat=data.ndim))
        real = dwtn(data.real, wavelet, mode)
        imag = dwtn(data.imag, wavelet, mode)
        return dict((k, real[k] + 1j * imag[k]) for k in keys)

    if data.dtype == np.dtype('object'):
        raise TypeError("Input must be a numeric array-like")
    if data.ndim < 1:
        raise ValueError("Input data must be at least 1D")

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    mode = Modes.from_object(mode)

    coeffs = [('', data)]
    for axis in range(data.ndim):
        new_coeffs = []
        for subband, x in coeffs:
            cA, cD = dwt_axis(x, wavelet, mode, axis)
            new_coeffs.extend([(subband + 'a', cA),
                               (subband + 'd', cD)])
        coeffs = new_coeffs
    return dict(coeffs)


def idwtn(coeffs, wavelet, mode='symmetric'):
    """
    Single-level n-dimensional Discrete Wavelet Transform.

    Parameters
    ----------
    coeffs: dict
        Dictionary as in output of `dwtn`. Missing or None items
        will be treated as zeroes.
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode used in the decomposition,
        see Modes (default: 'symmetric').

    Returns
    -------
    data: ndarray
        Original signal reconstructed from input data.

    """
    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    mode = Modes.from_object(mode)

    # Ignore any invalid keys
    coeffs = dict((k, np.asarray(v)) for k, v in coeffs.items()
                  if v is not None and set(k) <= set('ad'))

    if any(np.iscomplexobj(v) for v in coeffs.values()):
        real_coeffs = dict((k, v.real) for k, v in coeffs.items())
        imag_coeffs = dict((k, v.imag) for k, v in coeffs.items())
        return (idwtn(real_coeffs, wavelet, mode)
                + 1j * idwtn(imag_coeffs, wavelet, mode))

    dims = max(len(key) for key in coeffs.keys())

    try:
        coeff_shapes = (v.shape for k, v in coeffs.items()
                        if v is not None and len(k) == dims)
        coeff_shape = next(coeff_shapes)
    except StopIteration:
        raise ValueError("`coeffs` must contain at least one non-null wavelet "
                         "band")
    if any(s != coeff_shape for s in coeff_shapes):
        raise ValueError("`coeffs` must all be of equal size (or None)")

    for axis in reversed(range(dims)):
        new_coeffs = {}
        new_keys = [''.join(coeff) for coeff in product('ad', repeat=axis)]

        for key in new_keys:
            L = coeffs.get(key + 'a', None)
            H = coeffs.get(key + 'd', None)

            new_coeffs[key] = idwt_axis(L, H, wavelet, mode, axis)
        coeffs = new_coeffs

    return coeffs['']


def swt2(data, wavelet, level, start_level=0):
    """
    2D Stationary Wavelet Transform.

    Parameters
    ----------
    data : ndarray
        2D array with input data
    wavelet : Wavelet object or name string
        Wavelet to use
    level : int
        How many decomposition steps to perform
    start_level : int, optional
        The level at which the decomposition will start (default: 0)

    Returns
    -------
    coeffs : list
        Approximation and details coefficients::

            [
                (cA_n,
                    (cH_n, cV_n, cD_n)
                ),
                (cA_n+1,
                    (cH_n+1, cV_n+1, cD_n+1)
                ),
                ...,
                (cA_n+level,
                    (cH_n+level, cV_n+level, cD_n+level)
                )
            ]

        where cA is approximation, cH is horizontal details, cV is
        vertical details, cD is diagonal details and n is start_level.

    """
    data = np.asarray(data)
    if data.ndim != 2:
        raise ValueError("Expected 2D data array")

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    ret = []
    for i in range(start_level, start_level + level):
        # filter rows
        H, L = [], []
        for row in data:
            cA, cD = swt(row, wavelet, level=1, start_level=i)[0]
            L.append(cA)
            H.append(cD)

        # filter columns
        H = np.transpose(H)
        L = np.transpose(L)

        LL, LH = [], []
        for row in L:
            cA, cD = swt(row, wavelet, level=1, start_level=i)[0]
            LL.append(cA)
            LH.append(cD)

        HL, HH = [], []
        for row in H:
            cA, cD = swt(row, wavelet, level=1, start_level=i)[0]
            HL.append(cA)
            HH.append(cD)

        # build result structure: (approx, (horizontal, vertical, diagonal))
        approx = np.transpose(LL)
        ret.append((approx,
                    (np.transpose(LH), np.transpose(HL), np.transpose(HH))))

        # for next iteration
        data = approx

    return ret
