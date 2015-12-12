def swt(data, object wavelet, object level=None, int start_level=0):
    """
    swt(data, wavelet, level=None, start_level=0)

    Performs multilevel Stationary Wavelet Transform.

    Parameters
    ----------
    data :
        Input signal
    wavelet :
        Wavelet to use (Wavelet object or name)
    level : int, optional
        Transform level.
    start_level : int, optional
        The level at which the decomposition will begin (it allows one to
        skip a given number of transform steps and compute
        coefficients starting from start_level) (default: 0)

    Returns
    -------
    coeffs : list
        List of approximation and details coefficients pairs in order
        similar to wavedec function::

            [(cAn, cDn), ..., (cA2, cD2), (cA1, cD1)]

        where ``n`` equals input parameter `level`.

        If *m* = *start_level* is given, then the beginning *m* steps are skipped::

            [(cAm+n, cDm+n), ..., (cAm+1, cDm+1), (cAm, cDm)]

    """
    if np.iscomplexobj(data):
        data = np.asarray(data)
        coeffs_real = swt(data.real, wavelet, level, start_level)
        coeffs_imag = swt(data.imag, wavelet, level, start_level)
        coeffs_cplx = []
        for (cA_r, cD_r), (cA_i, cD_i) in zip(coeffs_real, coeffs_imag):
            coeffs_cplx.append((cA_r + 1j*cA_i, cD_r + 1j*cD_i))
        return coeffs_cplx

    # accept array_like input; make a copy to ensure a contiguous array
    dt = _check_dtype(data)
    data = np.array(data, dtype=dt)
    return _swt(data, wavelet, level, start_level)
