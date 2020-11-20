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

# Mock a sample user
test_user_r7 = User(
    email='test_frontend@test.com',
    name='Test_frontend$',
    password=generate_password_hash('test_frontend')
)

class FrontEndHomePageTest(BaseCase):

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
        self.assert_text("Welcome test frontend!", "#welcome-header")
        # reload the root page
        self.open(base_url + '/')
        # open /login
        self.open(base_url + '/login')
        # validate that we are on the correct profile page
        assert self.get_current_url() == base_url + '/'
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test frontend!", "#welcome-header")

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
        self.assert_text("Welcome test frontend!", "#welcome-header")

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
        self.assert_text("Welcome test frontend!", "#welcome-header")

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
        self.assert_text("Welcome test frontend!", "#welcome-header")

    @patch('qa327.backend.get_user', return_value=test_userR1)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR1)
    def test_login_password_format(self, *_):
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
        self.assert_element("#welcome-header")
        self.assert_text("Welcome test frontend!", "#welcome-header")
        
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
        self.type("#sell-expiry", "10/02/2020")
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
        self.type("#buy-name", "Test Show")
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
        self.type("#update-name", "Baby")
        self.type("#update-quantity", "25")
        self.type("#update-price", "30")
        self.type("#update-expiry", '10/20/2020')
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
