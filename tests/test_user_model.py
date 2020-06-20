import unittest
from app_code.models import User
from app_code import db
import time

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
    def test_generateToken(self):
        u1 = User(password = 'cat')
        u2 = User(password = 'dog')
        db.session.add(u1,u2)
        db.session.commit()
        token =u1.generate_confirmation_token()
        self.assertTrue(u1.confirm(token))
        self.assertFalse(u2.confirm(token))
    def test_confirmedAttribute(self):
        u1 = User(password = 'cat')
        db.session.add(u1)
        db.session.commit()
        token =u1.generate_confirmation_token()
        u1.confirm(token)
        self.assertTrue(u1.confirmed == True)
    def test_expirationTokeTime(self):
        u = User(password = 'tiger')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))
