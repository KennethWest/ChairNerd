import time

import pytest
from flask import session
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


class FrontEndHomePageTest(BaseCase):

    @patch('qa327.backend.get_user', return_value=test_userR3)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR3)
    def test_login_success(self, *_):
        """
        This is a sample front end unit test to login to home page
        and verify if the tickets are correctly listed.
        """
        # open login page
        self.open(base_url + '/login')
        # fill email and password
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
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
        self.assert_text("Hi test frontend!", "#welcome-header")
        self.assert_element("#tickets div h4")
        self.assert_text("t1 100 5 test1@gmail.com", "#tickets div h4")

    @patch('qa327.backend.get_user', return_value=test_userR3)
    @patch('qa327.backend.get_all_tickets', return_value=test_ticketsR3)
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
        self.assert_text("password format is incorrect", "#message")

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
        self.open(base_url + '/logout')

