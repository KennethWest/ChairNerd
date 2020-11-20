import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the frontend homepage.

The tests will only test the frontend portion of the program, by patching the backend to return
specfic values. For example:

@patch('qa327.backend.get_user', return_value=test_user)

Will patch the backend get_user function (within the scope of the current test case)
so that it return 'test_user' instance below rather than reading
the user from the database.

Annotate @patch before unit tests can mock backend methods (for that testing function)
"""

# Mock a sample user
test_user_r7 = User(
    email='test_frontend@test.com',
    name='Test_frontend$',
    password=generate_password_hash('test_frontend')
)

# Moch some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100'}
]


class FrontEndHomePageTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_success(self, *_):
        """
        This is a sample front end unit test to login to home page
        and verify if the tickets are correctly listed.
        """
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "test_frontend")
        # click enter button
        self.click('input[type="submit"]')

        # after clicking on the browser (the line above)
        # the front-end code is activated
        # and tries to call get_user function.
        # The get_user function is supposed to read data from database
        # and return the value. However, here we only want to test the
        # front-end, without running the backend logics.
        # so we patch the backend to return a specific user instance,
        # rather than running that program. (see @ annotations above)

        # open home page
        self.open(base_url)
        # test if the page loads correctly
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test_frontend", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100", "#tickets div h4")

    @patch('qa327.backend.get_user', return_value=test_user)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_password_failed(self, *_):
        """ Login and verify if the tickets are correctly listed."""
        # open login page
        self.open(base_url + '/login')
        # fill wrong email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "wrong_password")
        # click enter button
        self.click('input[type="submit"]')
        # make sure it shows proper error message
        self.assert_element("#message")
        self.assert_text("login failed", "#message")

    #R7.1 : Logout will invalid the current session and redirect to the login page. After logout, the user shouldn't be able to access restricted pages.
    @patch('qa327.backend.get_user', return_value=test_user_r7)
    def test_logout_redirect_to_login(self, *_):
    	self.open(base_url + '/logout')
    	self.open(base_url + '/login')
    	self.type("#email", "test_frontend@test.com")
    	self.type("#password", "Test_frontend$")
    	self.click('input[type="submit"]')
    	self.open(base_url)
    	self.open(base_url + '/logout')
    	self.open(base_url)
    	self.assert_element("#message")
    	self.assert_text("Please login", "#message")

    #R8.1 : For any other requests except /login, /register, /, /login, /buy, /sell, the system should return a 404 error
    def test_other_requests_are_404_errors(self, *_):
    	self.open(base_url + '/logout')
    	self.assert_no_404_errors()
    	self.open(base_url)
    	self.assert_no_404_errors()
    	self.open(base_url + '/login')
    	self.assert_no_404_errors()
    	self.open(base_url + '/register')
    	self.assert_no_404_errors()
    	self.open(base_url + '/fake_domain')
    	self.assert_element("#message")
    	self.assert_text("Uh Oh! Something is not quite right here, maybe you tried to access a page you do not have access to or one that has recently been deleted.", "#message")



