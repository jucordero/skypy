import numpy as np
import pytest
from astropy.cosmology import Planck15, FlatLambdaCDM
from skypy.power_spectrum import eisenstein_hu


def test_eisenstein_hu():
    """ Test Eisenstein & Hu Linear matter power spectrum with
    and without wiggles using Planck15 cosmology"""
    cosmology = Planck15
    A_s = 2.1982e-09
    n_s = 0.969453
    kwmap = 0.02

    # Test that a scalar input gives a scalar output
    scalar_input = 1
    scalar_output_w = eisenstein_hu(scalar_input, A_s, n_s, cosmology, kwmap,
                                    wiggle=True)
    scalar_output_nw = eisenstein_hu(scalar_input, A_s, n_s, cosmology, kwmap,
                                     wiggle=False)
    assert np.isscalar(scalar_output_w)
    assert np.isscalar(scalar_output_nw)

    # Test that an array input gives an array output
    array_shape = (10,)
    array_input = np.random.uniform(size=array_shape)
    array_output_w = eisenstein_hu(array_input, A_s, n_s, cosmology, kwmap,
                                   wiggle=True)
    array_output_nw = eisenstein_hu(array_input, A_s, n_s, cosmology, kwmap,
                                    wiggle=False)
    assert array_output_w.shape == array_shape
    assert array_output_nw.shape == array_shape

    # Test pk against precomputed values for Planck15 cosmology
    wavenumber = np.logspace(-3, 1, num=5, base=10.0)
    pk_eisensteinhu_w = eisenstein_hu(wavenumber, A_s, n_s, cosmology, kwmap,
                                      wiggle=True)
    pk_eisensteinhu_nw = eisenstein_hu(wavenumber, A_s, n_s, cosmology, kwmap,
                                       wiggle=False)
    pk_cosmosis_w = np.array([9.29895009e+03, 4.10421883e+04, 5.62046151e+03,
                              4.63533349e+01, 1.41107939e-01])
    pk_cosmosis_nw = np.array([9.29660250e+03, 4.17746880e+04, 5.54047525e+03,
                              4.55237583e+01, 1.38127599e-01])

    assert np.allclose(pk_eisensteinhu_w, pk_cosmosis_w)
    assert np.allclose(pk_eisensteinhu_nw, pk_cosmosis_nw)

    # Test for failure when wavenumber <= 0
    negative_wavenumber_scalar = 0
    with pytest.raises(ValueError):
        eisenstein_hu(negative_wavenumber_scalar, A_s, n_s, cosmology, kwmap,
                      wiggle=True)
    with pytest.raises(ValueError):
        eisenstein_hu(negative_wavenumber_scalar, A_s, n_s, cosmology, kwmap,
                      wiggle=False)
    negative_wavenumber_array = [0, 1, -2, 3]
    with pytest.raises(ValueError):
        eisenstein_hu(negative_wavenumber_array, A_s, n_s, cosmology, kwmap,
                      wiggle=True)
    with pytest.raises(ValueError):
        eisenstein_hu(negative_wavenumber_array, A_s, n_s, cosmology, kwmap,
                      wiggle=False)

    # Test for failure when cosmology has Ob0 = 0 and wiggle = True
    zero_ob0_cosmology = FlatLambdaCDM(H0=70, Om0=0.3, Tcmb0=2.725)
    wavenumber = np.logspace(-3, 1, num=5, base=10.0)
    with pytest.raises(ValueError):
        eisenstein_hu(wavenumber, A_s, n_s, zero_ob0_cosmology, kwmap,
                      wiggle=True)

    # Test for failure when cosmology has Tcmb = 0  and wiggle = True
    zero_Tcmb0_cosmology = FlatLambdaCDM(H0=70, Om0=0.3, Ob0=0.05)
    wavenumber = np.logspace(-3, 1, num=5, base=10.0)
    with pytest.raises(ValueError):
        eisenstein_hu(wavenumber, A_s, n_s, zero_Tcmb0_cosmology, kwmap,
                      wiggle=True)
