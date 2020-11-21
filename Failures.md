# First check failures: #

Error #1: 
R3.10.1 : The ticket-buying form can be posted to /buy
The output was wrong because it was not posting "Ticket successfully bought" to /buy.
The reason it was doing this was because the ticket "Test Show" did not exist. When this test was originally being 
tested, "Test Show" was in the database so it did exist but after merging it with the other code, that database was erased. To fix this, the code was modified by filling the sell form out first with the ticket "Test Show" that I want to buy, and THEN filling out the buy form.

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

Error #2:
R1.2.3 and R1.2.5: The final assert was checking for the text "Welcome test frontend!" despite us changing the text to "Hi test frontend!" Changing the test case code to match the desgin removed the failure
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

Error #3:
R1.2.6: Some test case code was cut off before the last line, specifically the code typing in the password and clicking the submit button. Code checking the #welcome-header text was also missing. Replacing this code fixed the failure
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

Error #4:
R1.2.1: The final assert was checking for the text "Welcome test frontend!" despite us changing the text to "Hi test frontend!" Changing the test case code to match the desgin removed the failure
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

Error #5:
R1.1.3: The final assert was checking for the text "Welcome test frontend!" despite us changing the text to "Hi test frontend!" Changing the test case code to match the desgin removed the failure
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
Error #6: 
R3.11.1 : The ticket-update form can be posted to /update 
The output was wrong because it was not posting "Ticket successfully updated" to /update.
The reason it was doing this was because the ticket "Baby" did not exist. When this test was originally being 
tested, "Baby" was in the database so it did exist but after merging it with the other code, that database was erased. To fix this, the code was modified by filling the sell form out first with the ticket "Baby" that I want to sell, and THEN filling out the update form to update that ticket. 
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
