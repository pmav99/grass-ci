# -*- coding: utf-8 -*-
import os.path

from grass.gunittest.case import TestCase


PARENT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(PARENT_DIR, "data")


class TestRFillStats(TestCase):

    ascii = 'ascii'
    stats = 'stats'
    wmean = 'wmean'
    mean = 'mean'
    median = 'median'
    mode = 'mode'

    @classmethod
    def setUpClass(cls):
        cls.use_temp_region()
        cls.runModule('r.in.ascii', input=os.path.join(DATA_DIR, 'input_ascii.txt'), output=cls.ascii, type='CELL')
        cls.runModule('r.in.ascii', input=os.path.join(DATA_DIR, 'output_wmean.txt'), output=cls.wmean, type='DCELL')
        cls.runModule('r.in.ascii', input=os.path.join(DATA_DIR, 'output_mean.txt'), output=cls.mean, type='DCELL')
        cls.runModule('r.in.ascii', input=os.path.join(DATA_DIR, 'output_median.txt'), output=cls.median, type='DCELL')
        cls.runModule('r.in.ascii', input=os.path.join(DATA_DIR, 'output_mode.txt'), output=cls.mode, type='CELL')
        cls.runModule('g.region', raster=cls.ascii)

    @classmethod
    def tearDownClass(cls):
        cls.del_temp_region()
        cls.runModule('g.remove', flags='f', type='raster',
                      name=[cls.ascii, cls.stats, cls.wmean, cls.mean, cls.median, cls.mode])

    def test_stats(self):
        """Test if results match verified rasters"""
        self.assertModule('r.fill.stats', input=self.ascii, output=self.stats, distance=1, mode='wmean', power=2, cells=2, overwrite=True)
        self.assertRastersNoDifference(self.stats, self.wmean, precision=1e-6)
        self.assertModule('r.fill.stats', input=self.ascii, output=self.stats, distance=1, mode='mean', power=2, cells=2, overwrite=True)
        self.assertRastersNoDifference(self.stats, self.mean, precision=1e-6)
        self.assertModule('r.fill.stats', input=self.ascii, output=self.stats, distance=1, mode='median', power=2, cells=2, overwrite=True)
        self.assertRastersNoDifference(self.stats, self.median, precision=1e-6)
        self.assertModule('r.fill.stats', input=self.ascii, output=self.stats, distance=1, mode='mode', power=2, cells=2, overwrite=True)
        self.assertRastersNoDifference(self.stats, self.mode, precision=1e-6)

if __name__ == '__main__':
    import grass.gunittest.main
    grass.gunittest.main.test()
