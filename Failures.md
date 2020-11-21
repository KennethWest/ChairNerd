# First check failures: #

R3.10.1
```
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
>       self.assert_text("Ticket successfully bought", "#message")
```

R1.2.3 and R1.2.5
```
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
>       self.assert_text("Welcome test frontend!", "#welcome-header")
```

R1.2.6
```
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
>       self.assert_element("#welcome-header")
```

R1.2.1
```
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
>       self.assert_text("Welcome test frontend!", "#welcome-header")
```

R1.1.3
```
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
>       self.assert_text("Welcome test frontend!", "#welcome-header")
```

R3.11.1
```
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
>       self.assert_text("Ticket successfully updated", "#message")
```
