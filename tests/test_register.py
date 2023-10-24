import unittest
import sys
import os

p = os.path.abspath(os.path.join(".."))
sys.path.append(p)

# flake8: noqa
from src.frontend.ui_register import registerHandler
from src.backend.database.database_user import UserDB


class TestRegisterHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.udb = UserDB()

    def test_empty_fields(self):
        """
        Test when one or more registration fields are empty.
        """
        result = registerHandler("", "password", "password", "student")
        self.assertEqual(result, (False, "One or more fields empty"))

    def test_password_mismatch(self):
        """
        Test when passwords provided by the user do not match.
        """
        result = registerHandler("user", "password1", "password2", "student")
        self.assertEqual(result, (False, "Passwords do not match"))

    def test_username_taken(self):
        """
        Test when the provided username is already taken.
        """
        result = registerHandler("teststd", "password", "password", "student")
        self.assertEqual(result, (False, "Username already taken"))

    def test_username_password_match(self):
        """
        Test when the username and password are the same.
        """
        result = registerHandler("user", "user", "user", "student")
        self.assertEqual(result, (False, "Username cannot be password"))

    def test_successful_registration_student(self):
        """
        Test successful registration of a student.
        """
        result = registerHandler("new_user", "password", "password", "student")
        self.assertEqual(result, (True, "Register Successful"))

    def test_successful_registration_educator(self):
        """
        Test successful registration of an educator.
        """
        result = registerHandler("new_user", "password", "password",
                                 "educator")
        self.assertEqual(result, (True, "Register Successful"))

    def test_correct_output_data_type(self):
        """
        Test for correct output datatype.
        """
        username = "new_user"
        password = "password"
        confirm_pw = "password"
        user_type = "student"

        out = registerHandler(username, password, confirm_pw, user_type)

        self.assertTrue(isinstance(out[0], bool),
                        "Output datatype must be (bool, str)")
        self.assertTrue(isinstance(out[1], str),
                        "Output datatype must be (bool, str)")
        
    def test_user_in_database(self):
        """
        Test if the user is correctly added into the database.
        """
        username = "new_user"
        password = "password"
        user_type = "student"

        registerHandler(username, password, password, user_type)

        user_from_db = self.udb.fetch_attr("username", username)
        self.assertIsNotNone(user_from_db, "User not found in database.")

    @classmethod
    def tearDown(cls):
        """
        Tries to remove database test entry after every test
        """
        try:
            cls.udb.remove_entry("new_user")
        except UserDB.EntryNotFoundException:
            pass

if __name__ == '__main__':
    unittest.main()
