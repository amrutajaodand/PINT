#!/usr/bin/env python
from __future__ import division, absolute_import, print_function

import unittest
from pint.solar_system_ephemerides import objPosVel_wrt_SSB, objPosVel
import numpy as np
import astropy.time as time
import os

from pinttestdata import testdir, datadir
os.chdir(datadir)

class TestSolarSystemDynamic(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        MJDREF = 2400000.5
        J2000_JD = 2451545.0
        J2000_MJD = J2000_JD - MJDREF
        SECPERJULDAY = 86400.0
        ets = np.random.uniform(0.0, 9000.0, 100000) * SECPERJULDAY
        mjd = J2000_MJD + ets / SECPERJULDAY
        self.tdb_time = time.Time(mjd, scale='tdb', format='mjd')
        self.ephem = ['de405', 'de421', 'de434', 'de430','de436']
        self.planets = ['jupiter', 'saturn', 'venus', 'uranus']

    # Here we only test if any errors happens.
    def test_earth(self):
        for ep in self.ephem:
            a = objPosVel_wrt_SSB('earth', self.tdb_time ,ephem = ep)
            assert a.obj == 'earth'
            assert a.pos.shape == (3, 100000)
            assert a.vel.shape == (3, 100000)

    def test_sun(self):
        for ep in self.ephem:
            a = objPosVel_wrt_SSB('sun', self.tdb_time ,ephem = ep)
            assert a.obj == 'sun'
            assert a.pos.shape == (3, 100000)
            assert a.vel.shape == (3, 100000)

    def test_planets(self):
        for p in self.planets:
            for ep in self.ephem:
                a = objPosVel_wrt_SSB(p, self.tdb_time ,ephem = ep)
                assert a.obj == p
                assert a.pos.shape == (3, 100000)
                assert a.vel.shape == (3, 100000)

    def test_earth2obj(self):
        objs = self.planets + ['sun']
        for obj in objs:
            for ep in self.ephem:
                a = objPosVel('earth', obj, self.tdb_time, ep)
                assert a.obj == obj
                assert a.origin == 'earth'
                assert a.pos.shape == (3, 100000)
                assert a.vel.shape == (3, 100000)
