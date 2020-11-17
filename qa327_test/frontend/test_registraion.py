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
test_userR1 = User(
    email='test_frontend@test.com',
    name='test frontend',
    password=generate_password_hash('Testfrontend#')
)

# Moch some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100'}
]


class FrontEndHomePageTest(BaseCase):

    #################
    # R1 test cases #
    #################
    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_redirect_from_base(self, *_):
        """
        Test case R1.1.1
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url)
        # validate that the user is taken to /login
        self.assert_text('Log In', 'h1')


    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_prompt_message(self, *_):
        """
        Test case R1.1.2
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # validate that the user is shown a message that says 'please login'
        self.assert_element('#message')
        self.assert_text('Please login', '#message')

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.login_user', return_value=True) # force a login;should crash
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_redirect_to_user_page_if_logged_in(self, *_):
        """
        Test case R1.1.3
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
        # validate that we are on the correct profile page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test frontend!", "#welcome-header")
        # reload the root page
        self.open(base_url + '/')
        # open /login
        self.open(base_url + '/login')
        # validate that we are on the correct profile page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test frontend!", "#welcome-header")

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_email_password_field_exists(self, *_):
        """
        Test case R1.1.4
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # validate that there are two elements for email and password in which text can be entered
        self.assert_element('#email')
        self.assert_element('#password')

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_post(self, *_):
        """
        Test case R1.2.1
        """
        # make sure we're logged out
        self.open('/logout')
        # open /login
        self.open(base_url + '/login')
        # type in login info
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that we are on the correct profile page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test frontend!", "#welcome-header")

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_email_password_must_exist(self, *_):
        """
        Test case R1.2.2
        """
        # make sure we're logged out
        self.open('/logout')
        # open /login
        self.open(base_url + '/login')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that we are still on /login
        self.assert_text('Log In', 'h1')

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_email_format(self, *_):
        """
        Test case R1.2.3
        """
        # make sure we're logged out
        self.open('/logout')
        # open /login
        self.open(base_url + '/login')
        # enter in a wrong format email and a correct format password
        self.type('#email', 'notanemail')
        self.type('#password', 'GoodPassword#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that the correct error message is displayed
        self.assert_text('email format is incorrect', '#message')
        # enter in a correct format email and a correct format password
        self.type('#email', 'test@example.com')
        self.type('#password', 'GoodPassword#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that the correct error message is displayed
        assert self.get_text('#message') != 'email format is incorrect'

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_password_format(self, *_):
        """
        Test case R1.2.4
        """
        # make sure we're logged out
        self.open('/logout')
        # open /login
        self.open(base_url + '/login')
        # enter in a correct format email and a wrong format password
        self.type('#email', 'test@example.com')
        self.type('#password', 'badpass')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that the correct error message is displayed
        self.assert_text('password format is incorrect', '#message')
        # enter in a correct format email and a correct format password
        # these credentials should not exist, #message should show a "user not found" related error
        self.type('#email', 'test@example.com')
        self.type('#password', 'GoodPassword#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that the correct error message is displayed
        assert self.get_text('#message') != 'password format is incorrect'

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    def test_login_password_format(self, *_):
        """
        Test case R1.2.6
        """
        # make sure we're logged out
        self.open('/logout')
        # open /login
        self.open(base_url + '/login')
        # enter incorrect credentials
        self.type('#email', 'wrong@email.com')
        self.type('#password', 'WrongPassword#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that the correct error message is displayed
        self.assert_text('email/password combination incorrect', '#message')
        # enter correct credentials
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that we are on the correct profile page
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test frontend!", "#welcome-header")

    # @patch('qa327.backend.get_user', return_value=test_user)
    # @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    # def test_login_success(self, *_):
    #     """
    #     This is a sample front end unit test to login to home page
    #     and verify if the tickets are correctly listed.
    #     """
    #     # open login page
    #     self.open(base_url + '/login')
    #     # fill email and password
    #     self.type("#email", "test_frontend@test.com")
    #     self.type("#password", "test_frontend")
    #     # click enter button
    #     self.click('input[type="submit"]')
    #
    #     # after clicking on the browser (the line above)
    #     # the front-end code is activated
    #     # and tries to call get_user function.
    #     # The get_user function is supposed to read data from database
    #     # and return the value. However, here we only want to test the
    #     # front-end, without running the backend logics.
    #     # so we patch the backend to return a specific user instance,
    #     # rather than running that program. (see @ annotations above)
    #
    #     # open home page
    #     self.open(base_url)
    #     # test if the page loads correctly
    #     self.assert_element("#welcome-header")
    #     self.assert_text("Welcome test_frontend", "#welcome-header")
    #     self.assert_element("#tickets div h4")
    #     self.assert_text("t1 100", "#tickets div h4")

    # @patch('qa327.backend.get_user', return_value=test_user)
    # @patch('qa327.backend.get_all_tickets', return_value=test_tickets)
    # def test_login_password_failed(self, *_):
    #     """ Login and verify if the tickets are correctly listed."""
    #     # open login page
    #     self.open(base_url + '/login')
    #     # fill wrong email and password
    #     self.type("#email", "test_frontend@test.com")
    #     self.type("#password", "wrong_password")
    #     # click enter button
    #     self.click('input[type="submit"]')
    #     # make sure it shows proper error message
    #     self.assert_element("#message")
    #     self.assert_text("login failed", "#message")
