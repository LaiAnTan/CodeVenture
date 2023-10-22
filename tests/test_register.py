import unittest
import sys
import os

p = os.path.abspath(os.path.join(".."))
sys.path.append(p)

from src.frontend.ui_register import registerHandler

class TestRegisterHandler(unittest.TestCase):
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
        result = registerHandler("testuser", "password", "password", "student")
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
        result = registerHandler("new_user", "password", "password", "educator")
        self.assertEqual(result, (True, "Register Successful"))

if __name__ == '__main__':
    unittest.main()