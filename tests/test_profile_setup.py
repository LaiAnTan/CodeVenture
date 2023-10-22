import unittest
import sys
import os

p = os.path.abspath(os.path.join(".."))
sys.path.append(p)

# flake8: noqa
from src.frontend.ui_student_profile_setup import profileSetupHandler
from src.backend.database.database_student import StudentDB
from src.backend.user.user_student import Student


class TestProfileSetupHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Setup before tests
        """
        cls.student = Student("unittest")
        cls.sdb = StudentDB()
        cls.params = ["unit test", "unittest@gmail.com",
                      "10/10/2000", "unittest.jpg"]

    def testEmpty(self):
        """
        Test for empty parameters
        """
        for i in range(len(self.params)):
            curr = self.params.copy()
            curr[i] = ""

            out = profileSetupHandler(self.student, curr[0], curr[1], curr[2],
                                      curr[3])

            self.assertFalse(out[0], "Empty parameters failed")

    def testInvalidEmail(self):
        """
        Test for invalid email address
        """
        curr = self.params.copy()
        curr[1] = "invalid email"

        out = profileSetupHandler(self.student, curr[0], curr[1], curr[2],
                                  curr[3])

        self.assertFalse(out[0], "Invalid email failed")

    def testValidParameters(self):
        """
        Test for valid parameters
        """
        out = profileSetupHandler(self.student, self.params[0], self.params[1],
                                  self.params[2], self.params[3])

        self.assertTrue(out[0], "Valid parameters failed")

    def testCorrectOutputDatatype(self):
        """
        Test for correct output datatype
        """
        out = profileSetupHandler(self.student, self.params[0], self.params[1],
                                  self.params[2], self.params[3])

        self.assertTrue(isinstance(out[0], bool),
                        "Output datatype must be (bool, str)")
        self.assertTrue(isinstance(out[1], str),
                        "Output datatype must be (bool, str)")

    def testDatabaseUpdated(self):
        """
        Test for updated database
        """
        profileSetupHandler(self.student, self.params[0], self.params[1],
                            self.params[2], self.params[3])

        self.assertTrue(self.sdb.fetch_attr("username",
                                            self.student.getUsername()) ==
                        self.student.getUsername(),
                        "Database is not updated")

    @classmethod
    def tearDown(cls):
        """
        Tries to remove database test entry after every test
        """
        try:
            cls.sdb.remove_entry(cls.student.getUsername())
        except StudentDB.EntryNotFoundException:
            pass


if __name__ == "__main__":
    unittest.main()
