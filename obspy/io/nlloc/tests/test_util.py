#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA @UnusedWildImport

import inspect
import os
import unittest

import numpy as np
try:
    import pyproj
    HAS_PYPROJ = True
except ImportError:
    HAS_PYPROJ = False

from obspy.io.nlloc.util import read_nlloc_scatter


def _coordinate_conversion(x, y, z):
    proj_wgs84 = pyproj.Proj(init="epsg:4326")
    proj_gk4 = pyproj.Proj(init="epsg:31468")
    x, y = pyproj.transform(proj_gk4, proj_wgs84, x*1e3, y*1e3)
    return x, y, z


class NLLOCTestCase(unittest.TestCase):
    """
    Test suite for obspy.io.nlloc
    """
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(inspect.getfile(
            inspect.currentframe())))
        self.datapath = os.path.join(self.path, "data")

    def test_read_nlloc_scatter_plain(self):
        """
        Test reading NLLoc scatter file without coordinate conversion.
        """
        # test without coordinate manipulation
        filename = os.path.join(self.datapath, "nlloc.scat")
        got = read_nlloc_scatter(filename)
        filename = os.path.join(self.datapath, "nlloc_scat.npy")
        expected = np.load(filename)
        np.testing.assert_array_equal(got, expected)

    @unittest.skipIf(not HAS_PYPROJ, 'pyproj not installed')
    def test_read_nlloc_scatter_coordinate_conversion(self):
        """
        Test reading NLLoc scatter file including coordinate conversion.
        """
        # test including coordinate manipulation
        filename = os.path.join(self.datapath, "nlloc.scat")
        got = read_nlloc_scatter(
            filename, coordinate_converter=_coordinate_conversion)
        filename = os.path.join(self.datapath, "nlloc_scat_converted.npy")
        expected = np.load(filename)
        np.testing.assert_array_equal(got, expected)


def suite():
    return unittest.makeSuite(NLLOCTestCase, "test")


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
