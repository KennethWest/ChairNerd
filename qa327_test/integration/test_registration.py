import pytest
from seleniumbase import BaseCase

from ChairNerd.qa327_test.conftest import base_url
from ChairNerd.qa327_test.conftest import base_url
from unittest.mock import patch
from ChairNerd.qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


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

    def test_register_login(self):
        """ This test checks the implemented login/logout feature """
        self.register()
        self.login()
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test0", "#welcome-header")


test_userR2_to_register = User(
    email='test_frontend@test.com',
    name='test frontend',
    password=generate_password_hash('Testfrontend#')
)

test_userR2_to_register_diff_email = User(
    email='test_frontende@test.com',
    name='test frontend',
    password=generate_password_hash('Testfrontend#')
)


class RegistrationPage(BaseCase):
    """
    Going to do the first registration test at the end after everything has been registered effectively.
    """

    def test_redirect_to_user_page_if_logged_in(self, *_):
        """
        Test case R2.1.1
        If user is logged in, it will simply redirect the user back to the profile page if they go on /register
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
        assert self.get_current_url() == base_url + '/'
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test frontend!", "#welcome-header")
        # reload the root page
        self.open(base_url+'/register')
        # validate that we are on the correct profile page
        assert self.get_current_url() == base_url + '/'
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test frontend!", "#welcome-header")

    def test_register_route_works(self, *_):
        """
        Test case R2.2.1
       Show the registration page if not logged in.
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.assert_text('Log In', 'Register')

    def test_register_shows_fields(self, *_):
        """
        Test case R2.3.1
        the registration page shows a registration form requesting: email, user name, password, password2
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.assert_element('#email')
        self.assert_element("#name")
        self.assert_element("#password")
        self.assert_element("#password2")
    #
    # @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    # def test_register_input_and_post(self, *_):
    #     """
    #     Test case R2.4.1
    #     Registered successfully.
    #     """
    #     self.open(base_url + '/logout')
    #     # go to main page
    #     self.open(base_url + '/register')
    #     # validate that the user is taken to /login
    #     assert self.get_current_url() == base_url + '/register'
    #     self.type('#email', 'test_frontend@test.com')
    #     self.type('#password', 'Testfrontend#')
    #     self.type('#password2', 'Testfrontend#')
    #     self.type('#name', 'test frontend')
    #     self.click('input[type="submit"]')
    #     assert self.get_current_url() == base_url + '/login'
    #     self.assert_text('message', "Please login")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_password_do_not_match(self, *_):
        """
        Test case R2.6.1
        Both passwords inputted do not match
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend')
        self.type('#name', 'test frontend')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "The passwords do not match")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_post_and_passwords_bad_no_spec_chars(self, *_):
        """
        Test case R2.5.1
        Passwords are not strong enough because of a lack of special characters
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend')
        self.type('#password2', 'Testfrontend')
        self.type('#name', 'test frontend')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Password not strong enough")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_post_and_passwords_bad_no_caps(self, *_):
        """
        Test case R2.5.2
        Passwords are not strong enough because of a lack of capital letters
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'testfrontend#')
        self.type('#password2', 'testfrontend#')
        self.type('#name', 'test frontend')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Password not strong enough")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_post_and_passwords_bad_no_lower(self, *_):
        """
        Test case R2.5.3
        Passwords are not strong enough because of a lack of lowercase characters
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'TESTFRONTEND#')
        self.type('#password2', 'TESTFRONTEND#')
        self.type('#name', 'test frontend')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Password not strong enough")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_post_and_passwords_bad_short(self, *_):
        """
        Test case R2.5.4
        Passwords are not strong enough because too short
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Te#')
        self.type('#password2', 'Te#')
        self.type('#name', 'test frontend')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Password not strong enough")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_post_and_email_bad(self, *_):
        """
        Test case R2.5.6
        Email format is incorrect
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontendtest.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', 'test frontend')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Email format is incorrect")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_user_name_empty(self, *_):
        """
        Test case R2.7.1
        User name is empty
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', ' ')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Name format is incorrect.")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_user_name_has_improper_space_in_beg(self, *_):
        """
        Test case R2.7.2
        User name has a space character as the first character
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', ' hello')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Name format is incorrect.")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_user_name_has_improper_space_in_end(self, *_):
        """
        Test case R2.7.3
        User name has a space character as the last character
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', 'hello ')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Name format is incorrect.")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_user_name_has_non_alphanumeric(self, *_):
        """
        Test case R2.7.4
        User name has a special character
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', 'hel@lo')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Name format is incorrect.")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_user_name_too_short(self, *_):
        """
        Test case R2.8.1
        User name is too short
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', 'h')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Name format is incorrect.")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_user_name_too_long(self, *_):
        """
        Test case R2.8.2
        Email format is incorrect
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', 'thisusernameismorethantwentycharacterslong')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Name format is incorrect.")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_email_already_used(self, *_):
        """
        Test case R2.10.1
        Email has already been used.
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontendee@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', 'hello')
        self.click('input[type="submit"]')
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontendee@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', 'hello')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "this email has been ALREADY used.")

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register_diff_email)
    def test_register_input_and_everything_works(self, *_):
        """
        Test case R2.11.1
        Everything works and we need to ensure that the balance is $5000.
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontende@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', 'hello')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('message', "Please login")
        self.type('#email', 'test_frontende@test.com')
        self.type('#password', 'Testfrontend#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that we are on the correct profile page
        assert self.get_current_url() == base_url + '/'
        self.assert_text("Your balance is: $5000", "balance")
