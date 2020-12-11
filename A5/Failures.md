# First check failures: #
## Table Summary
| Error Number | Test name                           | Specification | What the output was | What the error was        | How the error was fixed                                                                                                                  |
|--------------|-------------------------------------|---------------|---------------------|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| #1           | test_update_quantity_negative_fails | R5.3.2        | Update successful   | Update should have failed | Python condition chaining was not giving the correct output when checking for invalid inputs. Expanding the conditions solved the issues |
| #2           | test_update_quantity_over_100_fails | R5.3.2        | ""                  | ""                        | ""                                                                                                                                       |
| #3           | test_update_quantity_zero_fails     | R5.3.2        | ""                  | ""                        | ""                                                                                                                                       |
| #4           | test_update_date_fails              | R5.5.2        | ""                  | ""                        | ""                                                                                                                                       |
| #5           | test_update_price_gt_100_fails      | R5.4.2        | ""                  | ""                        | ""                                                                                                                                       |
| #6           | test_update_price_lt_10_fails       | R5.4.2        | ""                  | ""                        | ""                                                                                                                                       |

Error #1-6: 
R5.3.2, R5.5.4, R5.4.2.
All test cases failed in a similar way: error checking was allowing invalid inputs to pass.
This was due to a lack of understanding on how Python condition chaining worked. An
example of a condition that was incorrect was (10 > price > 100). Replacing this with (if 10 > price or price > 100)
solved the issue
```python
    #R5.3.2	Check if the updating actions fail when the quantity of tickets is over 100
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_update_quantity_over_100_fails(self, *_):
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Lia Ticket")
        self.type("#sell-quantity", "50")
        self.type("#sell-price", "75")
        self.type("#sell-expiry", "2020/02/10")
        self.click('input[id="sell-submit"]')
        self.type("#update-get-ticket", "Lia Ticket")
        self.type("#update-quantity", "420")
        self.click('input[id="update-submit"]')
        self.assert_element("#message")
        self.assert_text("Error: Number of tickets must be between 1 and 100", "#message")

    #R5.3.2	Check if the updating actions fail when the quantity of tickets is zero.
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_update_quantity_zero_fails(self, *_):
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Lia Ticket")
        self.type("#sell-quantity", "50")
        self.type("#sell-price", "75")
        self.type("#sell-expiry", "2020/02/10")
        self.click('input[id="sell-submit"]')
        self.type("#update-get-ticket", "Lia Ticket")
        self.type("#update-quantity", "0")
        self.click('input[id="update-submit"]')
        self.assert_element("#message")
        self.assert_text("Error: Number of tickets must be between 1 and 100", "#message")

    #R5.3.2	Check if the updating actions fail when the quantity of tickets is negative.
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_update_quantity_negative_fails(self, *_):
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Lia Ticket")
        self.type("#sell-quantity", "50")
        self.type("#sell-price", "75")
        self.type("#sell-expiry", "2020/02/10")
        self.click('input[id="sell-submit"]')
        self.type("#update-get-ticket", "Lia Ticket")
        self.type("#update-quantity", "-500")
        self.click('input[id="update-submit"]')
        self.assert_element("#message")
        self.assert_text("Error: Number of tickets must be between 1 and 100", "#message")

    #R5.4.2	Check if the updating actions fail when the price of a ticket is less than 10
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_update_price_lt_10_fails(self, *_):
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Lia Ticket")
        self.type("#sell-quantity", "50")
        self.type("#sell-price", "75")
        self.type("#sell-expiry", "2020/02/10")
        self.click('input[id="sell-submit"]')
        self.type("#update-get-ticket", "Lia Ticket")
        self.type("#update-price", "5")
        self.click('input[id="update-submit"]')
        self.assert_element("#message")
        self.assert_text("Error: Ticket price must be between 10 and 100 (inclusive)", "#message")

    #R5.4.2	Check if the updating actions fail when the price of a ticket is greater than 100
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_update_price_gt_100_fails(self, *_):
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Lia Ticket")
        self.type("#sell-quantity", "50")
        self.type("#sell-price", "75")
        self.type("#sell-expiry", "2020/02/10")
        self.click('input[id="sell-submit"]')
        self.type("#update-get-ticket", "Lia Ticket")
        self.type("#update-price", "420")
        self.click('input[id="update-submit"]')
        self.assert_element("#message")
        self.assert_text("Error: Ticket price must be between 10 and 100 (inclusive)", "#message")

    #R5.5.2	Check if the updating actions fail when the date is in any other format
    @patch('qa327.backend.get_user', return_value=test_userR3)
    def test_update_date_fails(self, *_):
        self.open(base_url + '/logout')
        self.open(base_url + '/login')
        self.type("#email", "test_frontend@test.com")
        self.type("#password", "Testfrontend#")
        self.click('input[type="submit"]')
        self.open(base_url)
        self.type("#sell-name", "Lia Ticket")
        self.type("#sell-quantity", "50")
        self.type("#sell-price", "75")
        self.type("#sell-expiry", "2020/02/10")
        self.click('input[id="sell-submit"]')
        self.type("#update-get-ticket", "Lia Ticket")
        self.type("#update-expiry", "19982801")
        self.click('input[id="update-submit"]')
        self.assert_element("#message")
        self.assert_text("Error: Date must be given in the format YYYYMMDD", "#message")
```