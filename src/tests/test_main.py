"""
Tests the main module
"""

import os
import sys
import unittest

_p = os.sep.join(__file__.split(os.sep)[:-2])
if _p not in sys.path:
    sys.path.append(_p)


class TestMain(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
