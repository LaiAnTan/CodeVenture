import unittest
import sys
import os

p = os.path.abspath(os.path.join('..'))
sys.path.append(p)



class TestModuleParsing(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
    """
    Couple of set ups for testing
    """
        pass


    @classmethod
    def tearDownClass(cls) -> None:
        """
        Remove test assets aftet done testing
        """
        pass
