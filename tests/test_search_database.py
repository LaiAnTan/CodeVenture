import unittest
import sys
import os

p = os.path.abspath(os.path.join(".."))
sys.path.append(p)

# flake8: noqa

from src.backend.activity.ac_functions import search_database

class TestSearchDatabase(unittest.TestCase):

    def test_search_existing_module(self):
        """
        Test searching for an existing module in the database
        """
        module = search_database("world")
        self.assertIsNotNone(module)
        self.assertEqual(type(module), list,
                         "Returned is not a list")
        for entry in module:
            self.assertEqual(type(entry), tuple,
                             "Entry is not a tuple")
            self.assertEqual(len(entry), 2,
                             "Entry is not a tuple of length 2")
            self.assertEqual(type(entry[0]), str,
                             "Entry does not have a string module code")
            self.assertEqual(entry[0], "CH0000",
                             "Entry does not have the correct module code")
            self.assertEqual(type(entry[1]), int,
                             "Entry does not have a integer difficulty index")
            self.assertEqual(entry[1], 2)


    def test_search_nonexistent_module(self):
        """
        Test searching for a module that does not exist in the database
        """
        module = search_database("test world a")
        self.assertEqual(module, [],
                         "Returned is not an empty list")

    def test_search_empty_module(self):
        """
        Test searching for a module with an empty module name
        """
        module = search_database("")
        test = [('MD0000', 1), ('QZ0000', 3), ('CH0000', 2), ('CH0001', 2),
                ('CH0002', 2)]
        for entry in module:
            self.assertEqual(len(entry), 2,
                             "Entry is not a tuple of length 2")
        self.assertEqual(module, test,
                         "Returned is not a list of all modules")

    def test_search_invalid_module(self):
        """
        Test searching for a module with an invalid module name
        (e.g. containing special characters)
        """
        module = search_database("\n\t\0")
        self.assertEqual(module, [],
                         "Returned is not an empty list")

if __name__ == '__main__':
    unittest.main()