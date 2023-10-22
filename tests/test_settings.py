import unittest
import sys
import os

p = os.path.abspath(os.path.join(".."))
sys.path.append(p)

from src.frontend.ui_settings import changePasswordHandler
from src.backend.user.user_student import Student


class TestChangePasswordHandler(unittest.TestCase):
    def test_empty_fields(self):
        """
        Test when one or more password change fields are empty.
        """
        result = changePasswordHandler(student=None, old_password="", new_password="", confirm_password="")
        self.assertEqual(result, (False, "One or more fields empty"))

    def test_old_password_same_as_new_password(self):
        """
        Test when the old password is the same as the new password.
        """
        result = changePasswordHandler(student=None, old_password="password", new_password="password", confirm_password="password")
        self.assertEqual(result, (False, "Old password same as new password"))

    def test_new_password_mismatch(self):
        """
        Test when new password and confirm password do not match.
        """
        result = changePasswordHandler(student=None, old_password="old_pw", new_password="new_pw", confirm_password="incorrect_pw")
        self.assertEqual(result, (False, "Passwords do not match"))

    def test_wrong_old_password(self):
        """
        Test when the provided old password is incorrect.
        """
        result = changePasswordHandler(student=None, old_password="incorrect_pw", new_password="new_pw", confirm_password="new_pw")
        self.assertEqual(result, (False, "Wrong password"))

    def test_successful_password_change(self):
        """
        Test a successful password change.
        """
        # Assuming student object and correct old password
        student = Student(username="testuser", password="testuser")
        result = changePasswordHandler(student=student, old_password="testuser", new_password="new_password", confirm_password="new_password")
        self.assertEqual(result, (True, "Password Change Successful"))

if __name__ == '__main__':
    unittest.main()