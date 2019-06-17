"""
Tests the controller module
"""

import os
import sys
import unittest

_p = os.sep.join(__file__.split(os.sep)[:-2])
if _p not in sys.path:
    sys.path.append(_p)
from pd.controller import Manager, RenderFacade, IoFacade


_pj = os.path.join
_pd = os.path.dirname


class TestManager(unittest.TestCase):

    def setUp(self):
        self._dirname = _pd(_pd(_pd(__file__)))
        self._infile = _pj(self._dirname, 'data', 'test.xml')

    def test_supported_formats(self):
        self.assertItemsEqual(Manager.supported_formats(),
                              ['json', 'xml']
                              )

    def test_supported_renderers(self):
        self.assertItemsEqual(Manager.supported_renderers(),
                              ['console', 'html']
                              )

    def test_convert_source_file(self):
        outfile = _pj(self._dirname, 'output', 'test_out.json')
        manager1 = Manager(self._infile, outfile)
        data1 = manager1.load_file()
        self.assertTrue(data1)
        self.assertTrue(manager1.convert_source_file())

        manager2 = Manager(outfile, None)
        data2 = manager2.load_file()
        self.assertTrue(data2)
        self.assertEqual(data1, data2)

    def test_render_data(self):
        _test_str = """\

Source data path: 'C:\\Users\\jcochrane\\Documents\\git\\test-al-file-handling\\data\\test.xml'
=========================================================================================

################################################################################
id: 101
   city: BRUNSWICK NORTH
   name: Gambardella, Matthew
   phone_no: (03) 9902 4163
   street: Ocean street
   postcode: 3056
   house_no: 67

"""

        manager = Manager(self._infile)
        manager.load_file()

        manager.render_data()
        self.assertMultiLineEqual(manager.output_value, _test_str)


if __name__ == '__main__':
    # suite = unittest.TestSuite()
    # suite.addTest(TestController("test_render_data"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    unittest.main()

    # _dirname = _pd(_pd(__file__))
    # _infile = _pj(_dirname, 'data', 'test.xml')
    # manager = Manager(_infile)
    # manager.load_file()
    # manager.render_data()
    # print manager.output_value
