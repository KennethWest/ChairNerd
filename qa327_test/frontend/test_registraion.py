import time

import pytest
from flask import session
import pdb
from seleniumbase import BaseCase
from sqlalchemy.sql.functions import user
from werkzeug.utils import redirect

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


test_userR1 = User(
    email='test_frontend@test.com',
    name='test frontend',
    password=generate_password_hash('Testfrontend#')
)

# Mock some sample tickets
test_ticketsR1 = [
    {'name': 't1', 'price': '100'}
]

# Moch a sample user
test_userR3 = User(
    email='test_frontend@test.com',
    name='test frontend',
    password=generate_password_hash('Testfrontend#'),
    balance=5000
)

# Moch some sample tickets
test_ticketsR3 = [
    {'name': 't1', 'price': '100', 'quantity': '5', 'owner': 'test1@gmail.com'}
]

# Moch a sample user
test_userR4 = User(
    email='test_frontend@test.com',
    name='test frontend',
    password=generate_password_hash('Testfrontend#'),
    balance=5000
)


# Mock a sample user
test_user_r7 = User(
    email='test_frontend@test.com',
    name='Test_frontend$',
    password=generate_password_hash('test_frontend')
)

class FrontEndHomePageTest(BaseCase):

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

    #################
    # R1 test cases #
    #################
    def test_login_redirect_from_base(self, *_):
        """
        Test case R1.1.1
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # go to main page
        self.open(base_url)
        # validate that the user is taken to /login
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('Log In', 'h1')

    def test_login_prompt_message(self, *_):
        """
        Test case R1.1.2
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # validate that we are on /login
        assert self.get_current_url() == base_url + '/login'
        # validate that the user is shown a message that says 'please login'
        self.assert_element('#message')
        self.assert_text('Please login', '#message')

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR1)
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
        assert self.get_current_url() == base_url + '/'
        self.assert_element("#welcome-header")
        self.assert_text("Hi test frontend!", "#welcome-header")
        # reload the root page
        self.open(base_url + '/')
        # open /login
        self.open(base_url + '/login')
        # validate that we are on the correct profile page
        assert self.get_current_url() == base_url + '/'
        self.assert_element("#welcome-header")
        self.assert_text("Hi test frontend!", "#welcome-header")

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
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR1)
    def test_login_post(self, *_):
        """
        Test case R1.2.1
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
        self.assert_text("Hi test frontend!", "#welcome-header")

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR1)
    def test_email_password_must_exist(self, *_):
        """
        Test case R1.2.2
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that we are still on /login
        assert self.get_current_url() == base_url + '/login'
        self.assert_text('Log In', 'h1')

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR1)
    def test_login_email_format(self, *_):
        """
        Test case R1.2.3 and R1.2.5
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter in a wrong format email and a correct format password
        self.type('#email', 'notanemail')
        self.type('#password', 'GoodPassword#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that we were not rerouted
        assert self.get_current_url() == base_url + '/login'
        # validate that the correct error message is displayed
        self.assert_text('email format is incorrect', '#message')
        # enter in a correct email and a correct password
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that we are on the correct profile page
        assert self.get_current_url() == base_url + '/'
        self.assert_element("#welcome-header")
        self.assert_text("Hi test frontend!", "#welcome-header")

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR1)
    def test_login_password_format(self, *_):
        """
        Test case R1.2.4 and R1.2.5
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
        # open /login
        self.open(base_url + '/login')
        # enter in a correct format email and a wrong format password
        self.type('#email', 'test@example.com')
        self.type('#password', 'badpass')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that the correct error message is displayed
        self.assert_text('password format is incorrect', '#message')
        # enter in a correct email and a correct password
        self.type('#email', 'test_frontend@test.com')
        self.type('#password', 'Testfrontend#')
        # click the log in button
        self.click('input[type="submit"]')
        # validate that we are on the correct profile page
        assert self.get_current_url() == base_url + '/'
        self.assert_element("#welcome-header")
        self.assert_text("Hi test frontend!", "#welcome-header")

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR1)
    def test_login_password_and_email_format(self, *_):
        """
        Test case R1.2.6
        """
        # make sure we're logged out
        self.open(base_url + '/logout')
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
        assert self.get_current_url() == base_url + '/'
        self.assert_element("#welcome-header")
        self.assert_text("Hi test frontend!", "#welcome-header")
        
    #################
    # R3 test cases #
    #################
    # R3.1.1: If the user is not logged in, redirect to login page
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_redirected_to_login_page(self, *_):
        # logout to make sure no user is logged in
        self.open(base_url + "/logout")
        # open user home page
        self.open(base_url)
        self.assert_element("#message")
        self.assert_text("Please login", "#message")
        self.open(base_url + '/logout')

    # R3.2.1: This page shows a header 'Hi {}'.format(user.name)
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_shows_header_hi_name(self, *_):
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_element("#welcome-header")
        self.assert_text("Hi test frontend!", "#welcome-header")
        self.open(base_url + '/logout')


    # R3.3.1: The page shows user balance
    @patch('qa327.backend.get_user', return_value=test_userR3)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR3)
    def test_shows_user_balance(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        balance = str(test_userR3.balance)
        self.assert_element("#balance-header")
        self.assert_text("Your balance is: $" + balance, "#balance-header")
        self.open(base_url + '/logout')

    # R3.4.1: The page show a logout link, pointing to /logout
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_logout_link(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.is_link_text_visible("logout")
        self.click_link_text("logout", timeout=None)
        self.assert_element("#message")
        self.assert_text("Please login", "#message")
        self.open(base_url + '/logout')

    # R3.5.1: The page lists all available tickets (includes quantity, email, price)
    @patch('qa327.backend.get_user', return_value=test_userR3)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR3)
    def test_available_tickets(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_element("#avail-tickets")
        self.assert_text("Here are all available tickets", "#avail-tickets")
        self.assert_element("#tickets")
        self.assert_text("t1 100 5 test1@gmail.com", "#tickets")
        self.open(base_url + '/logout')

    # R3.6.1: The page contains a form that a user can submit new tickets to sell (includes name, quantity, price,
    # expiration date)
    @patch('qa327.backend.get_user', return_value=test_userR3)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR3)
    def test_sell_form(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_element("#SellMsg")
        self.assert_text("Sell tickets:", "#SellMsg")
        self.open(base_url + '/logout')

    # R3.7.1: The page contains a form that a user can submit new tickets to buy(includes name, quantity)
    @patch('qa327.backend.get_user', return_value=test_userR3)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR3)
    def test_buy_form(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_element("#BuyMsg")
        self.assert_text("Buy tickets:", "#BuyMsg")
        self.open(base_url + '/logout')

    # R3.8.1: The page contains a form that a user can update new tickets to buy(includes ticket name, quantity,
    # price, expiry)
    @patch('qa327.backend.get_user', return_value=test_userR3)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR3)
    def test_update_form(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.assert_element("#UpdateMsg")
        self.assert_text("Update ticket:", "#UpdateMsg")
        self.open(base_url + '/logout')

    # R3.9.1: The ticket-selling form can be posted to /sell ###
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_sell_form_post(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Test Show")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/10/02")
        # click enter button
        self.click('input[id="sell-submit"]')
        self.assert_element("#message")
        self.assert_text("Ticket successfully posted to sell", "#message")
        self.open(base_url + '/logout')

    # R3.10.1: The ticket-buying form can be posted to /buy ###
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_buy_form_post(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Example")
        self.type("#sell-quantity", "20")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/10/02")
        # click enter button
        self.click('input[id="sell-submit"]')
        self.type("#buy-name", "Example")
        self.type("#buy-quantity", "10")
        # click enter button
        self.click('input[id="buy-submit"]')
        self.assert_element("#message")
        self.assert_text("Ticket successfully bought", "#message")
        self.open(base_url + '/logout')

    # R3.11.1: The ticket-update form can be posted to /update ###
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_update_form_post(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Another example")
        self.type("#sell-quantity", "20")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/10/02")
        # click enter button
        self.click('input[id="sell-submit"]')
        self.type("#update-name", "Another example")
        self.type("#update-quantity", "10")
        self.type("#update-price", "15")
        self.type("#update-expiry", '2020/10/25')
        # click enter button
        self.click('input[id="update-submit"]')
        self.assert_element("#message")
        self.assert_text("Ticket successfully updated", "#message")
        self.open(base_url + '/logout')

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

    # R4.1.1: /sell[POST] Check if the selling actions succeed when the ticket name is alphanumeric-only**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_succeeds_alphanumeric_only_ticket(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "TestShow")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        self.assert_element("#message")
        self.assert_text("Ticket successfully posted to sell", "#message")
        self.open(base_url + '/logout')

    # R4.1.2: /sell[POST] Check if the selling actions fail when the ticket names contain special characters**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_fails_special_characters_ticket(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "TestShow:)")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        assert self.get_current_url() == base_url + '/sell'
        self.assert_element("#message")
        self.assert_text("The name of the ticket has to be alphanumeric-only (and spaces allowed only if not the "
                         "first or last character)", "#message")
        self.open(base_url + '/logout')

    # R4.1.3: /sell[POST] Check if the selling actions succeed when the ticket names contain a space that is not the first or last character**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_succeeds_valid_space(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Test Show")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        self.assert_element("#message")
        self.assert_text("Ticket successfully posted to sell", "#message")
        self.open(base_url + '/logout')

    # R4.1.4: /sell[POST] Check if the selling actions fail when the ticket names contain a space as the first character, the last character, or both**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_fails_invalid_space(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", " TestShow")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        assert self.get_current_url() == base_url + '/sell'
        self.assert_element("#message")
        self.assert_text("Space allowed only if it is not the first or last character", "#message")
        self.open(base_url + '/logout')

    # R4.2.1: /sell[POST] Check if the selling actions succeed when the ticket name is less than 60 characters (but not empty) or exactly 60 characters**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_succeeds_ticket_valid_name_length(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "T")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        self.assert_element("#message")
        self.assert_text("Ticket successfully posted to sell", "#message")
        self.open(base_url + '/logout')

    # R4.2.2: /sell[POST] Check if the selling actions fail when the ticket name is more than 60 characters, or zero characters (empty)**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_fails_ticket_invalid_name_length(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Very long name that is more than 60 characters surely much longer")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        assert self.get_current_url() == base_url + '/sell'
        self.assert_element("#message")
        self.assert_text("The name of the ticket can be no longer than 60 characters", "#message")
        self.open(base_url + '/logout')

    # R4.3.1: /sell[POST] Check if the selling actions succeed when the quantity of the tickets is between 1 and 100 (inclusive)**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_succeeds_valid_ticket_quantity(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Test")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        self.assert_element("#message")
        self.assert_text("Ticket successfully posted to sell", "#message")
        self.open(base_url + '/logout')

    # R4.3.2: /sell[POST] Check if the selling actions fail when the quantity of tickets is over 100, is zero, or is negative**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_fails_ticket_quantity_gt_100(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Test")
        self.type("#sell-quantity", "105")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        assert self.get_current_url() == base_url + '/sell'
        self.assert_element("#message")
        self.assert_text("The quantity of tickets has to be more than 0 and less than or equal to 100", "#message")
        self.open(base_url + '/logout')

    # R4.3.2: /sell[POST] Check if the selling actions fail when the quantity of tickets is over 100, is zero, or is negative**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_fails_ticket_quantity_zero(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Test")
        self.type("#sell-quantity", "0")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        assert self.get_current_url() == base_url + '/sell'
        self.assert_element("#message")
        self.assert_text("The quantity of tickets has to be more than 0 and less than or equal to 100", "#message")
        self.open(base_url + '/logout')

    # R4.3.2: /sell[POST] Check if the selling actions fail when the quantity of tickets is over 100, is zero, or is negative**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_fails_ticket_quantity_negative(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Test")
        self.type("#sell-quantity", "-10")
        self.type("#sell-price", "25")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        assert self.get_current_url() == base_url + '/sell'
        self.assert_element("#message")
        self.assert_text("The quantity of tickets has to be more than 0 and less than or equal to 100", "#message")
        self.open(base_url + '/logout')

    # R4.4.1: /sell[POST] Check if the selling actions succeed when the price of a ticket is between 10 and 100 (inclusive)**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_succeeds_valid_ticket_price(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Test")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "10")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        self.assert_element("#message")
        self.assert_text("Ticket successfully posted to sell", "#message")
        self.open(base_url + '/logout')

    # R4.4.2: /sell[POST] Check if the selling actions fail when the price of a ticket is less than 10, or over 100**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_fails_invalid_ticket_price_lt_10(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Test")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "9")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        assert self.get_current_url() == base_url + '/sell'
        self.assert_element("#message")
        self.assert_text("The ticket price has to be between $10 and $100 (inclusive)", "#message")
        self.open(base_url + '/logout')

    # R4.4.2: /sell[POST] Check if the selling actions fail when the price of a ticket is less than 10, or over 100**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_fails_invalid_ticket_price_gt_100(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Test")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "101")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        assert self.get_current_url() == base_url + '/sell'
        self.assert_element("#message")
        self.assert_text("The ticket price has to be between $10 and $100 (inclusive)", "#message")
        self.open(base_url + '/logout')

    # R4.5.1: /sell[POST] Check if the selling actions succeed when the date is in the format YYYYMMDD**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_succeeds_valid_date_format(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Testing")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "15")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        self.assert_element("#message")
        self.assert_text("Ticket successfully posted to sell", "#message")
        self.open(base_url + '/logout')

    # R4.5.2: /sell[POST] Check if the selling actions fail when the date is in any other format (YYMMDD, YYYYMMD, YYYYDDMM, MMDDYYYY, DDMMYYYY etc)**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_selling_fails_invalid_date_format(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Testing")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "15")
        self.type("#sell-expiry", "10/02/2020")
        # click enter button
        self.click('input[id="sell-submit"]')
        assert self.get_current_url() == base_url + '/sell'
        self.assert_element("#message")
        self.assert_text("Expiry date must be given in the format YYYY/MM/DD", "#message")
        self.open(base_url + '/logout')

    # R4.6.1 and R4.6.2 have been incorporated into all of the test cases above for R4, for clarity and efficiency

    # R4.7.1: /sell[POST] The added new ticket information will be posted on the user profile page**
    @patch('qa327.backend.get_user', return_value=test_userR4)
    def test_new_ticket_info_posted(self, *_):
        self.open(base_url + '/logout')
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        # click enter button
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Good ticket")
        self.type("#sell-quantity", "10")
        self.type("#sell-price", "15")
        self.type("#sell-expiry", "2020/02/10")
        # click enter button
        self.click('input[id="sell-submit"]')
        self.assert_element("#message")
        self.assert_text("Ticket successfully posted to sell", "#message")
        self.assert_element("#tickets")
        self.assert_text("Good ticket 15.0 10 test_frontend@test.com 2020/02/10", "#tickets")
        self.open(base_url + '/logout')

