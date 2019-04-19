import os.path

from grass.gunittest.case import TestCase
from grass.gunittest.gmodules import call_module

PARENT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(PARENT_DIR, "data")

SMALL_MAP = """\
north:   15
south:   10
east:    25
west:    20
rows:    5
cols:    5

100.0 150.0 150.0 100.0 100.0
100.0 150.0 150.0 100.0 100.0
100.0 150.0 150.0 150.0 150.0
100.0 150.0 150.0 100.0 100.0
100.0 150.0 150.0 100.0 100.0
"""

class TestSlopeAspect(TestCase):

    slope_map = "limits_slope"
    aspect_map = "limits_aspect"

    def tearDown(self):
        self.remove_maps(rasters=[self.slope_map, self.aspect_map])

    def test_limits(self):
        self.assertModule('r.slope.aspect', elevation='elevation',
                          slope=self.slope_map, aspect=self.aspect_map)
        self.assertRasterMinMax(map=self.slope_map, refmin=0, refmax=90,
                                msg="Slope in degrees must be between 0 and 90")
        self.assertRasterMinMax(map=self.aspect_map, refmin=0, refmax=360,
                                msg="Aspect in degrees must be between 0 and 360")

    def test_limits_percent(self):
        """Assumes NC elevation and allows slope up to 100% (45deg)"""
        self.assertModule('r.slope.aspect', elevation='elevation',
                          slope=self.slope_map, aspect=self.aspect_map, format='percent')
        self.assertRasterMinMax(map=self.slope_map, refmin=0, refmax=100,
                                msg="Slope in percent must be between 0 and 100")
        self.assertRasterMinMax(map=self.aspect_map, refmin=0, refmax=360,
                                msg="Aspect in degrees must be between 0 and 360")


class TestSlopeAspectAgainstReference(TestCase):
    """

    Data created using::

        g.region n=20 s=10 e=25 w=15 res=1
        r.surf.fractal output=fractal_surf
        r.out.ascii input=fractal_surf output=data/fractal_surf.ascii
        gdaldem slope .../fractal_surf.ascii .../gdal_slope.grd -of GSAG
        gdaldem aspect .../fractal_surf.ascii .../gdal_aspect.grd -of GSAG -trigonometric

    GDAL version 1.11.0 was used. Note: GDAL-slope/aspect implementation is originally based on
    GRASS GIS 4.1.
    """

    # precision for comparisons
    precision = 0.0001

    # Maps that get cleared up in tearDownClass
    elevation_map = 'fractal_surf'
    # Maps that get cleared up in tearDown
    reference_map = 'reference_map'
    fractal_map = 'fractal_map'

    def tearDown(self):
        self.remove_maps(rasters=[self.reference_map, self.fractal_map])

    @classmethod
    def setUpClass(cls):
        cls.use_temp_region()
        call_module('g.region', n=20, s=10, e=25, w=15, res=1)
        cls.runModule('r.in.ascii', input=os.path.join(DATA_DIR, 'fractal_surf.ascii'),
                      output=cls.elevation_map)

    @classmethod
    def tearDownClass(cls):
        cls.del_temp_region()
        cls.remove_maps(rasters=cls.elevation_map)

    def test_slope(self):
        # TODO: using gdal instead of ascii because of cannot seek error
        self.runModule('r.in.gdal', flags='o',
                       input=os.path.join(DATA_DIR, 'gdal_slope.grd'), output=self.reference_map)
        self.assertModule('r.slope.aspect', elevation=self.elevation_map,
                          slope=self.fractal_map)
        # check we have expected values
        self.assertRasterMinMax(map=self.fractal_map, refmin=0, refmax=90,
                                msg="Slope in degrees must be between 0 and 90")
        # check against reference data
        self.assertRastersNoDifference(actual=self.fractal_map, reference=self.reference_map,
                                       precision=self.precision)

    def test_aspect(self):
        # TODO: using gdal instead of ascii because of cannot seek error
        self.runModule('r.in.gdal', flags='o',
                       input=os.path.join(DATA_DIR, 'gdal_aspect.grd'), output=self.reference_map)
        self.assertModule('r.slope.aspect', elevation=self.elevation_map,
                          aspect=self.fractal_map)
        # check we have expected values
        self.assertRasterMinMax(map=self.fractal_map, refmin=0, refmax=360,
                                msg="Aspect in degrees must be between 0 and 360")
        # check against reference data
        self.assertRastersNoDifference(actual=self.fractal_map, reference=self.reference_map,
                                       precision=self.precision)


class TestSlopeAspectAgainstItself(TestCase):

    precision = 0.0000001

    elevation_map = 'elevation'
    t_aspect = 'sa_together_aspect'
    t_slope = 'sa_together_slope'
    s_aspect = 'sa_separately_aspect'
    s_slope = 'sa_separately_slope'

    @classmethod
    def setUpClass(cls):
        cls.use_temp_region()
        call_module('g.region', raster=cls.elevation_map)

    @classmethod
    def tearDownClass(cls):
        cls.del_temp_region()

    def tearDown(self):
        maps = [self.t_aspect, self.t_slope, self.s_aspect, self.s_slope]
        self.remove_maps(rasters=maps)

    def test_slope_aspect_together(self):
        """Slope and aspect computed separately and together should be the same
        """
        self.assertModule('r.slope.aspect', elevation=self.elevation_map,
                          aspect=self.s_aspect)
        self.assertModule('r.slope.aspect', elevation=self.elevation_map,
                          slope=self.s_slope)
        self.assertModule('r.slope.aspect', elevation=self.elevation_map,
                          slope=self.t_slope, aspect=self.t_aspect)
        self.assertRastersNoDifference(actual=self.t_aspect, reference=self.s_aspect,
                                       precision=self.precision)
        self.assertRastersNoDifference(actual=self.t_slope, reference=self.s_slope,
                                       precision=self.precision)


# TODO: implement this class
class TestExtremes(TestCase):

    elevation_map = 'small_elevation'
    slope_map = 'small_slope'
    aspect_map = 'small_aspect'

    def setUp(self):
        self.use_temp_region()

    def tearDown(self):
        self.remove_maps(rasters=[self.elevation_map, self.slope_map, self.aspect_map])
        self.del_temp_region()

    def test_small(self):
        self.runModule('r.in.ascii', input='-', output=self.elevation_map,
                       stdin_=SMALL_MAP)
        call_module('g.region', raster=self.elevation_map)
        self.assertModule('r.slope.aspect', elevation=self.elevation_map,
                          slope=self.slope_map, aspect=self.aspect_map)
        self.assertRasterMinMax(map=self.slope_map, refmin=0, refmax=90,
                                msg="Slope in degrees must be between 0 and 90")
        self.assertRasterMinMax(map=self.aspect_map, refmin=0, refmax=360,
                                msg="Aspect in degrees must be between 0 and 360")


if __name__ == '__main__':
    import grass.gunittest.main
    grass.gunittest.main.test()
