import unittest
from app_code.models import User

class UserModelTestCase(unittest.TestCase):
    def test_userSetter(self):
        u = User(password = 'dog')
        self.assertTrue(u.pswd_hashed is not None)
    def test_getterNotReadable(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password
    def test_verifyPassword(self):
        u = User(password='bird')
        self.assertTrue(u.verify_pswd('bird'))
        self.assertFalse(u.verify_pswd('cat'))
    def test_samePassword_differentHash(self):
        u1 = User(password = 'cat')
        u2 = User(password = 'cat')
        self.assertFalse( u1.pswd_hashed == u2.pswd_hashed)