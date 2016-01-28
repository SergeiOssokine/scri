# Copyright (c) 2015, Michael Boyle
# See LICENSE file for details: <https://github.com/moble/scri/blob/master/LICENSE>

"""Module for operating on gravitational waveforms in various forms

Classes
-------
WaveformBase : Base class
    This is probably not needed directly; it is just used for inheritance by other objects.
WaveformModes: Complex spin-weighted spherical-harmonic modes
    The modes must include all `m` values for a range of `ell` values.  This is the "classic" version of a WaveformBase
    object we might normally think of.
WaveformGrid: Complex quantity evaluated along world lines of grid points on the sphere
    To perform translations or boosts, we need to transform to physical space, along a series of selected world lines
    distributed evenly across the sphere.  These values may need to be interpolated to new time values, and they will
    presumably need to be transformed back to `WaveformModes`.
WaveformInDetector: Real quantities as observed in an inertial detector
    Detectors only measure one polarization, so they deal with real quantities.  Also, data is measured in evenly
    spaced time steps.  This object can be created from a `WaveformModes` object.
WaveformInDetectorFT: (Complex) Fourier transform of a `WaveformInDetector`
    This contains only the positive-frequency values since the transformed data is real.

"""


from __future__ import print_function, division, absolute_import

import sys

from ._version import __version__

def version_info():
    """Show version information about this module and various dependencies"""
    import spherical_functions
    import quaternion
    import scipy
    import numba
    import numpy
    versions = '\n'.join(['scri.__version__ = {0}'.format(__version__),
                          'spherical_functions.__version__ = {0}'.format(spherical_functions.__version__),
                          'quaternion.__version__ = {0}'.format(quaternion.__version__),
                          'scipy.__version__ = {0}'.format(scipy.__version__),
                          'numba.__version__ = {0}'.format(numba.__version__),
                          'numpy.__version__ = {0}'.format(numpy.__version__)])
    return versions


# The speed of light is, of course, defined to be exact:
speed_of_light = 299792458.0  # m/s

# The value of the solar mass parameter G*M_sun is known to higher accuracy than either of its factors.  The value
# here is taken from the publication "2015 Selected Astronomical Constants", which can be found at
# <http://asa.usno.navy.mil/SecK/Constants.html>.  This is (one year more current than, but numerically the same as)
# the source cited by the Particle Data Group.  It is given as 1.32712440041e20 m^3/s^2 in the TDB (Barycentric
# Dynamical Time) time scale, which seems to be the more relevant one, and looks like the more standard one for LIGO.
# Dividing by the speed of light squared, we get the mass of the sun in meters; dividing again, we get the mass of
# the sun in seconds:
m_sun_in_meters = 1476.62503851  # m
m_sun_in_seconds = 4.92549094916e-06  # s

# By "IAU 2012 Resolution B2", the astronomical unit is defined to be exactly 1 au = 149597870700 m.  The parsec
# is, in turn, defined as "The distance at which 1 au subtends 1 arc sec: 1 au divided by pi/648000."  Thus, the
# future-proof value of the parsec in meters is
parsec_in_meters = 3.0856775814913672789139379577965e16  # m


FrameType = [UnknownFrameType, Inertial, Coprecessing, Coorbital, Corotating] = range(5)
FrameNames = ["UnknownFrameType", "Inertial", "Coprecessing", "Coorbital", "Corotating"]

DataType = [UnknownDataType, psi0, psi1, psi2, psi3, psi4, sigma, h, hdot, news, psin] = range(11)
DataNames = ["UnknownDataType", "psi0", "psi1", "psi2", "psi3", "psi4", "sigma", "h", "hdot", "news", "psin"]
SpinWeights = [sys.maxsize, 2, 1, 0, -1, -2, 2, -2, -2, -2, sys.maxsize]
ConformalWeights = [sys.maxsize, 2, 1, 0, -1, -2, 1, 0, -1, -1, -3]
RScaling = [sys.maxsize, 5, 4, 3, 2, 1, 2, 1, 1, 1, 0]
MScaling = [sys.maxsize, 2, 2, 2, 2, 2, 0, 0, 1, 1, 2]
DataNamesLaTeX = [r"\mathrm{unknown data type}", r"\psi_0", r"\psi_1", r"\psi_2", r"\psi_3", r"\psi_4", r"\sigma", r"h",
                  r"\dot{h}", r"\mathrm{n}", r"\psi_n"]
# It might also be worth noting that:
# - the radius `r` has spin weight 0 and boost weight -1
# - a time-derivative `d/du` has spin weight 0 and boost weight -1
# - \eth has spin weight +1; \bar{\eth} has spin weight -1
# - \eth in the GHP formalism has boost weight 0
# - \eth in the original NP formalism has undefined boost weight
# - It seems like `M` should have boost weight 1, but I'll have to think about the implications

# Set up the WaveformModes object, by adding some methods
from .waveform_modes import WaveformModes
from .mode_calculations import (LdtVector, LVector, LLComparisonMatrix, LLMatrix,
                                LLDominantEigenvector, angular_velocity)
WaveformModes.LdtVector = LdtVector
WaveformModes.LVector = LVector
WaveformModes.LLComparisonMatrix = LLComparisonMatrix
WaveformModes.LLMatrix = LLMatrix
WaveformModes.LLDominantEigenvector = LLDominantEigenvector
WaveformModes.angular_velocity = angular_velocity
from .rotations import rotate_decomposition_basis, rotate_physical_system
WaveformModes.rotate_decomposition_basis = rotate_decomposition_basis
WaveformModes.rotate_physical_system = rotate_physical_system

from .waveform_grid import WaveformGrid

from . import sample_waveforms, SpEC

__all__ = ['WaveformModes', 'WaveformGrid', 'WaveformInDetector',
           'FrameType', 'UnknownFrameType', 'Inertial', 'Coprecessing', 'Coorbital', 'Corotating', 'FrameNames',
           'DataType', 'UnknownDataType', 'psi0', 'psi1', 'psi2', 'psi3', 'psi4', 'sigma', 'h', 'hdot', 'news', 'psin',
           'DataNames', 'DataNamesLaTeX', 'SpinWeights', 'ConformalWeights', 'RScaling', 'MScaling',
           'speed_of_light', 'm_sun_in_meters', 'm_sun_in_seconds', 'parsec_in_meters']