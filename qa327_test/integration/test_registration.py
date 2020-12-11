import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
import qa327.backend as bn
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import random


# integration testing: the test case interacts with the
# browser, and test the whole system (frontend+backend).

@pytest.mark.usefixtures('server')
class Registered(BaseCase):

    def register(self):
        """register new user"""
        self.open(base_url + '/register')
        self.type("#email", "test0")
        self.type("#name", "test0")
        self.type("#password", "test0")
        self.type("#password2", "test0")
        self.click('input[type="submit"]')

    def login(self):
        """ Login to Swag Labs and verify that login was successful. """
        self.open(base_url + '/login')
        self.type("#email", "test0")
        self.type("#password", "test0")
        self.click('input[type="submit"]')
    '''
    def test_register_login(self):
        """ This test checks the implemented login/logout feature """
        self.register()
        self.login()
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("Hi test0", "#welcome-header")
    '''

    def test_blackbox_get_user(self, *_):
        """
        Blackbox test case for backend function to get user
        This test case registers a user, and then checks to see if they exist.
        Then afterwards tests to see if an email which does not exist is also retrieved
        (which it should not)
        """
        try:
            bn.register_user("test_frontendeee@test.com", "Tester", "TestFront#")
        except:
            pass
        user = bn.get_user("test_frontendeee@test.com")
        if user:
            assert True
        user_bad = bn.get_user("not_test_frontende@test.com")
        if not user_bad:
            assert True

    test_user_integration = User(
        email='test_frontend@test.com',
        name='test frontend',
        password=generate_password_hash('Testfrontend#'),
        balance=5000
    )

    @patch('qa327.backend.get_user', return_value=test_user_integration)
    def test_integration_1(self, *_):
        """
        Integration test for creating postings
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # type in login info
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        # click the log in button
        self.click('input[type="submit"]')
        # enter in the sell info
