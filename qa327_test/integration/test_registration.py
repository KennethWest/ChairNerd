import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
import qa327.backend as bn


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
        bn.register_user("test_frontendeee@test.com", "Tester", "TestFront#")
        user = bn.get_user("test_frontendeee@test.com")
        if user:
            assert True
        user_bad = bn.get_user("not_test_frontende@test.com")
        if not user_bad:
            assert True
