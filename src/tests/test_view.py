"""
Tests the view module
"""

import os
import sys
import unittest


_p = os.sep.join(__file__.split(os.sep)[:-2])
if _p not in sys.path:
    sys.path.append(_p)
del _p
from pd.view import HtmlWriter, TextWriter, RenderMaker


_pj = os.path.join
_pd = os.path.dirname


class TestView(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self._title = 'TITLE - <SOURCE_FILEPATH>'

    def test_text_writer(self):
        _test_str = """\
                                     TITLE
                                     =====
test: test_value

"""
        tw = TextWriter()
        rm = RenderMaker('TITLE', tw)
        rm.add_paragraph('test: test_value')
        rm.render()
        output = rm.output.getvalue()
        self.assertMultiLineEqual(_test_str, output)

    def test_html_writer(self):
        _test_str = """\
<!doctype html>
<html>
<head><title>TITLE - &lt;SOURCE_FILEPATH&gt;</title></head>
<body>
<p>test</p>
</body>
</html>
"""
        hw = HtmlWriter()
        rm = RenderMaker(self._title, hw)
        rm.add_paragraph('test')
        rm.render()
        self.assertMultiLineEqual(rm.output.getvalue(), _test_str)


if __name__ == '__main__':
    unittest.main()
