import unittest
import sys
import os

p = os.path.abspath(os.path.join(".."))
sys.path.append(p)

# flake8: noqa

from src.frontend.ui_settings import changePasswordHandler
from src.backend.user.user_student import Student
from src.backend.database.database_user import UserDB
from argon2 import PasswordHasher

class TestChangePasswordHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.student = Student("unittest")
        cls.udb = UserDB()
        ph = PasswordHasher()
        data = ("unittest", ph.hash("unittest"), "student")
        cls.udb.add_entry(data)

    def test_empty_fields(self):
        """
        Test when one or more password change fields are empty.
        """
        result = changePasswordHandler(self.student, "", "", "")
        self.assertEqual(result, (False, "One or more fields empty"))

    def test_old_password_same_as_new_password(self):
        """
        Test when the old password is the same as the new password.
        """
        result = changePasswordHandler(self.student, "password", "password",
                                       "password")
        self.assertEqual(result, (False, "Old password same as new password"))

    def test_new_password_mismatch(self):
        """
        Test when new password and confirm password do not match.
        """
        result = changePasswordHandler(self.student, "old_pw", "new_pw",
                                       "incorrect_pw")
        self.assertEqual(result, (False, "Passwords do not match"))

    def test_wrong_old_password(self):
        """
        Test when the provided old password is incorrect.
        """
        result = changePasswordHandler(self.student, "incorrect_pw", "new_pw",
                                       "new_pw")
        self.assertEqual(result, (False, "Wrong password"))

    def test_successful_password_change(self):
        """
        Test a successful password change.
        """
        result = changePasswordHandler(self.student, "unittest",
                                       "new_password", "new_password")
        self.assertEqual(result, (True, "Password Change Successful"))

    @classmethod
    def tearDownClass(cls):
        """
        Tries to remove database test entry after every test
        """
        try:
            cls.udb.remove_entry(cls.student.getUsername())
        except UserDB.EntryNotFoundException:
            pass

if __name__ == '__main__':
    unittest.main()