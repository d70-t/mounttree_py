from unittest import TestCase
import unittest
import numpy.testing as npt
import numpy as np
import sys as sys
sys.path.append('/home/p/Paul.Ockenfuss/Work/Software/mounttree_py/src/')
import mounttree_io as mio
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class TestMountTree(TestCase):
    def setUp(self):
        self.universe=mio.load_mounttree(os.path.join(basedir, 'testmounttree.yaml'))
    def test_updates(self):
        self.universe.update(lat=0, lon=0, height=10)
        earth=self.universe.get_frame('EARTH')
        npt.assert_almost_equal(self.universe.get_frame('HALO').pos, [0,0,10])
        tr1=self.universe.get_transformation('HALO','EARTH')
        self.universe.update(lat=0, lon=0, height=20)
        tr2=self.universe.get_transformation('HALO', 'EARTH')
        npt.assert_almost_equal(earth.toNatural(tr1.apply_point([0,0,0])),[0,0,10])
        npt.assert_almost_equal(earth.toNatural(tr2.apply_point([0,0,0])),[0,0,20])




if __name__=='__main__':
    unittest.main()

        
