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
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)

test_userR1 = User(
    email='test_frontend@test.com',
    name='test frontend',
    password=generate_password_hash('Testfrontend#')
)

# Mock some sample tickets
test_ticketsR1 = [
    {'name': 't1', 'price': '100'}
]

# Moch some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100'}
]

test_userR2_to_register = User(
    email='test_frontend@test.com',
    name='test frontend',
    password=generate_password_hash('Testfrontend#')
)

test_userR2_to_register_diff_email = User(
    email='test_frontende@test.com',
    name='hello',
    password=generate_password_hash('Testfrontend#')
)


class FrontEndHomePageTest(BaseCase):
    #
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
    #
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

    """SHREY'S TESTS"""
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
        self.assert_text('Register', 'h1')

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

    @patch('qa327.backend.register_user', return_value=test_userR2_to_register)
    def test_register_input_and_post(self, *_):
        """
        Test case R2.4.1
        Registered successfully.
        """
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url + '/register')
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/register'
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        self.type('#password2', 'Testfrontend#')
        self.type('#name', 'test frontend')
        self.click('input[type="submit"]')
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('Please login', "#message")

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
        assert self.get_current_url() == base_url + '/login?message=The+passwords+do+not+match'
        self.assert_text("The passwords do not match", "#message")

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
        #print("hello")
        assert self.get_current_url() == base_url + '/login?message=Password+not+strong+enough'
        self.assert_text("Password not strong enough", '#message')

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
        assert self.get_current_url() == base_url + '/login?message=Password+not+strong+enough'
        # assert self.get_current_url() == base_url + '/login'
        self.assert_text("Password not strong enough", '#message')

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
        assert self.get_current_url() == base_url + '/login?message=Password+not+strong+enough'
        self.assert_text("Password not strong enough", '#message')

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
        assert self.get_current_url() == base_url + '/login?message=Password+not+strong+enough'
        self.assert_text("Password not strong enough", '#message')

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
        assert self.get_current_url() == base_url + '/login?message=Email+format+is+incorrect'
        self.assert_text("Email format is incorrect", '#message')

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
        assert self.get_current_url() == base_url + '/login?message=Name+format+is+incorrect.'
        self.assert_text("Name format is incorrect.", '#message')


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
        assert self.get_current_url() == base_url + '/login?message=Name+format+is+incorrect.'
        self.assert_text("Name format is incorrect.", '#message')

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
        assert self.get_current_url() == base_url + '/login?message=Name+format+is+incorrect.'
        self.assert_text("Name format is incorrect.", '#message')

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
        assert self.get_current_url() == base_url + '/login?message=Name+format+is+incorrect.'
        self.assert_text("Name format is incorrect.", '#message')

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
        assert self.get_current_url() == base_url + '/login?message=Name+format+is+incorrect.'
        self.assert_text("Name format is incorrect.", '#message')

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
        assert self.get_current_url() == base_url + '/login?message=Name+format+is+incorrect.'
        self.assert_text("Name format is incorrect.", '#message')

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
        assert self.get_current_url() == base_url + '/login?message=this+email+has+been+ALREADY+used'
        self.assert_text("this email has been ALREADY used", '#message')


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
        self.open(base_url+'/login')
        assert self.get_current_url() == base_url + '/login'
        self.type('#email', 'test_frontende@test.com')
        self.type('#password', 'Testfrontend#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that we are on the correct profile page
        assert self.get_current_url() == base_url + '/'
        self.assert_text("Your balance is: $5000", "#balance-header")

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
        self.type('#email', 'test_frontende@test.com')
        self.type('#password', 'Testfrontend#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that we are on the correct profile page
        assert self.get_current_url() == base_url + '/'
        self.assert_element("#welcome-header")
        # reload the root page
        self.open(base_url + '/register')
        # validate that we are on the correct profile page
        assert self.get_current_url() == base_url + '/'
        self.assert_element("#welcome-header")
        self.assert_text("Welcome hello !", "#welcome-header")