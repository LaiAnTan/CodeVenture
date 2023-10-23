import unittest
import sys
import os

p = os.path.abspath(os.path.join(".."))
sys.path.append(p)

# flake8: noqa

from src.backend.activity.ac_functions import search_database, sort_results
from src.backend.database.database_activity import ActivityDB

class TestSortResults(unittest.TestCase):

    @classmethod
    def setUp(self):
        """
        Setup base database for testing
        """
        self.adb = ActivityDB()
        self.database = search_database("")
        self.assertTrue(self, self.database, msg="Database is empty!")
        
    def test_valid_sort(self):
        """
        Testing valid sorting of database results, with valid inputs of mode and option.
        """
        sorted_results = sort_results(self.database, "difficulty", "asc")
        for element in sorted_results:
            #checks if every element in the sorted results is a tuple 
            self.assertEqual(type(element), tuple, msg="Invalid sorting, did not return expected results for tuple format.")

            #checks if every element in the sorted results is a tuple with 2 elements
            self.assertEqual(len(element), 2, msg="Invalid sorting, tuple doesn't have 2 elements.")

            #checks if first element is a string
            self.assertEqual(type(element[0]), str, msg="Invalid sorting, first element of tuple is not a string.")

            #checks if second element is an integer
            self.assertEqual(type(element[1]), int, msg="Invalid sorting, second element of tuple is not an integer.")

            #checks if return element can be found in the original database
            self.assertIn(element, self.database, msg="Invalid sorting, did not found return element in database.")
            
            #checks if the difficulty of the current element is less than or equal to the next element
            self.assertGreaterEqual(self.adb.fetch_attr("difficulty", sorted_results[len(sorted_results)-1][0]), self.adb.fetch_attr("difficulty", element[0]), msg="Invalid sorting, difficulty of current element is greater than the next element.")
        
            # Sort by difficulty, ascending
            self.assertEqual(sort_results(self.database, "difficulty", "asc"), [('MD0000', 1), ('QZ0000', 3), ('CH0000', 2), ('CH0001', 2)],
                            msg = "Incorrect sorted results, different from expected results.")
    
    def test_invalid_sort(self):
        """
        Testing sorting function with invalid parameters.
        """
        
        #checks with invalid mode parameter
        self.assertEqual(sort_results(self.database, "testtest123", "asc"), [], msg="Invalid sorting, did not return empty list for invalid mode parameter.")

        #checks with invalid option parameter
        self.assertEqual(sort_results(self.database, "difficulty", "whatamicooking"), [], msg="Invalid sorting, did not return empty list for invalid option parameter.")

        #checks with empty mode and option parameters
        self.assertEqual(sort_results(self.database, "", ""), [], msg="Invalid sorting, did not return empty list for empty mode and option parameters.")


if __name__ == '__main__':
    unittest.main()
    # print(sort_results(search_database(""), "", ""))
