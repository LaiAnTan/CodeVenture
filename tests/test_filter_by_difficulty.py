import unittest
import sys
import os

p = os.path.abspath(os.path.join(".."))
sys.path.append(p)

# flake8: noqa

from src.backend.activity.ac_functions import search_database, filter_by_difficulty
from src.backend.database.database_activity import ActivityDB

class TestFilterByDifficulty(unittest.TestCase):

    @classmethod
    def setUp(self):
        """
        Setup base database for testing
        """
        self.adb = ActivityDB()
        self.database = search_database("")
        self.lower_limit = 5
        self.upper_limit = 10
        

    def test_valid_filter(self):
        """
        Test with valid filtering parameters and valid database.
        """
        self.assertTrue(self.database, msg="Database is empty!")
        filtered = filter_by_difficulty(self.database, self.upper_limit, self.lower_limit)
        expected = [('MD0000', 1), ('QZ0000', 3), ('CH0000', 2)]
        self.assertIsNotNone(filtered, msg="Filtered database returned NULL!")
        self.assertEqual(filtered, expected, msg="Invalid filtering, did not return expected results")
        for result in filtered:
            self.assertEqual(len(result), 2, msg="Invalid filtering, did not return expected results for tuple format.")
            diff = self.adb.fetch_attr("difficulty", result[0])
            self.assertTrue(diff <= self.upper_limit and diff >= self.lower_limit, msg="Invalid filtering")
    
    def test_negative_filter(self):
        """
        Test with negative filtering parameters and valid database.
        """
        self.lower_limit = -100
        self.upper_limit = -1
        filtered = filter_by_difficulty(self.database, self.upper_limit, self.lower_limit)
        expected = []
        self.assertIsNotNone(filtered, msg="Filtered database returned NULL!")
        self.assertEqual(filtered, expected, msg="Invalid filtering, did not return expected results")
    
    def test_empty_filter(self):
        """
        Test with empty filtering parameters and valid database.
        """
        self.lower_limit = 0
        self.upper_limit = 0
        filtered = filter_by_difficulty(self.database, self.upper_limit, self.lower_limit)
        expected = []
        self.assertIsNotNone(filtered, msg="Filtered database returned NULL!")
        self.assertEqual(filtered, expected, msg="Invalid filtering, did not return expected results")
    
    def test_invalid_filter(self):
        """
        Test with invalid filtering parameters and valid database.
        """
        self.lower_limit = "a"
        self.upper_limit = "b"
        filtered = filter_by_difficulty(self.database, self.upper_limit, self.lower_limit)
        expected = []
        self.assertIsNotNone(filtered, msg="Filtered database returned NULL!")
        self.assertEqual(filtered, expected, msg="Invalid filtering, did not return expected results")

    


if __name__ == '__main__':
    unittest.main()