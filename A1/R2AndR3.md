in# Ken's Test Cases R2 & R3 #

## Test Cases For R2: ##

### Test Case R2.1.1 - If a user is logged in, redirect back to the user profile page ###

Mocking:
- Mock backend.get_user to return a test_user instance

Actions:
- open /logout (to ensure there is no logged in user)
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="submit"]
- validate that current page is /
- open /logout

### Test Case R2.1.2 - Otherwise, show the user the registration page ###

Actions:
- open /logout (to ensure there is no logged in user)
- validate the current page is /register.
- open /logout

### Test Case R2.2.1 - The registration page shows a registration form requesting: email, user name, password, assword2 ###

Actions:
- open /logout (to ensure there is no logged in user)
- open /register
- validate the current page contains #email element.
- validate the current page contains #user-name element.
- validate the current page contains #password element.
- validate the current page contains #password2 element.
- open /logout

### Test Case R2.3.1 - The registration form can be submitted as a POST request to the current URL (/register) ###

Actions:
- open /logout (to ensure there is no logged in user)
- open /register
- enter create_user's email into element #email
- enter create_user's user-name into element #user-name
- enter create_user's password into element #password
- enter create_user's password again into element #password2
- click element input[type="submit"]
- validate that #register_message element shows successful
- validate that current page is now /login
- open /logout

### Test Case R2.4.1 - Email, password, password2 all satisfy the same requirements defined in R1 - Negative ###

Actions:
- open /logout
- open /register
- enter one of the following bellow to not meet the specifications outlined in R1:
- enter create_user's email into element #email
- enter create_user's password into element #password
- enter create_user's password2 into element #password2
- validate that #error_message element shows details on invalid input
- open /logout

### Test Case R2.4.2 - Email, password, password2 all satisfy the same requirements defined in R1 - Postitive ###

Actions:
- open /logout
- open /register
- enter all of the following bellow such that they meet the specifications outlined in R1:
- enter create_user's email into element #email
- enter create_user's password into element #password
- enter create_user's password2 into element #password2
- validate that element #green_check is displayed next to each input box
- open /logout

### Test Case R2.5.1 - Password and password2 have to be exactly the same - Negative ###

Actions:
- open /logout
- open /register
- enter create_user's password into element #password
- enter create_user's password into element #password2 such that it is not the same as what is in element #password
- validate that element #red_ex is next to the password boxes
- validate that element #error-message explains password mismatch
- open /logout

### Test Case R2.5.2 - Password and password2 have to be exactly the same - Positive ###

Actions:
- open /logout
- open /register
- enter create_user's password into element #password
- enter create_user's password into element #password2
- validate that element #green_check is displayed next to each input box
- open /logout

### Test Case R2.6.1 - Username has to be non-empty, alphanumeric-only, and space allowed only if its not the first or last character. Username has to be longer than 2 characters and less than 20 - Negative ###

Actions:
- open /logout
- open /register
- enter enter create_user's user-name such that it does not meet at least following specifications:
	- User-name must not be empty
	- User-name must be alphanumeric-only
	- User-name may contain a space only if its not the first an last character
	- User-name must be longer than 2 characters and less than 20.
- validate that the element #red_ex is displayed next to the username input box
- validate that the element #error-message explains invalid user-name entry
- open /logout

### Test Case R2.6.2 - Username has to be non-empty, alphanumeric-only, and space allowed only if its not the first or last character. Username has to be longer than 2 characters and less than 20 - Positive ###

Actions:
- open /logout
- open /register
- enter create_user's user-name such that it does meet all of the following specifications:
	- User-name must not be empty
	- User-name must be alphanumeric-only
	- User-name may contain a space only if its not the first an last character
	- User-name must be longer than 2 characters and less than 20.
- validate that the element #green_check is displayed next to the username input box
- open /logout


### Test Case R2.7.1 - For any formatting errors, redirect back to /login and show message '{} format is incorrect.'.format(the_corresponding_attribute) ###

Actions:
- open /logout
- open /register
- enter at least one of the follow in a way such that it does not mean the requirments tests in R2.4.1 - R2.6.2:
- enter create_user's email into the element #email
- enter create_user's user-name into the element #user-name
- enter create_user's password into the element #password
- enter create_user's password into the element #password2
- click element input[type="submit"]
- validate page redirects to /login
- validate #error-message element displays: '{} format is incorrect.'.format(the_corresponding_attribute), where the_corresponding_attribute is either email, password, or user-name.
- open /logout

### Test Case R2.8.1 - If the email already exists, show message 'this email has been ALREADY used' ###

Mocking:
- Mock backend.get_user to return a test_user instance

Actions:
- open /logout
- open /register
- enter test_user's email into the element #email
- validate #red_ex element is displayed next to element #email
- validate #error-message element displays: "This email is already in use. Please either login or enter another email."
- open /logout

### Test Case R2.9.1 - If no error regarding the inputs following the rules above, create a new user, set the balance to 5000, and go back to the /login page ###

Mocking:
- Mock backend.get_user to return test_user instance

Actions:
- open /logout
- open /register
- enter test_user's email into element #email
- enter test_user's user-name into element #user-name
- enter test_user's password into element #password
- enter test_user's password again into element #password2
- click element input[type="submit"]
- validate that #register_message element shows successful
- validate that current page is now /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- validate that current page is /
- validate that test_user balance is 5000.
- open /logout

## Test Cases For R3: ##

### Test Case R3.1.1 - If the user is not logged in, redirect to login page ###

Actions:
- open /logout
- open /
- validate that the current page is now redirected to /login
- open /logout

### Test Case R3.2.1 - This page shows a header 'Hi {}'.format(user.name) ###

Mocking:
- Mock backend.get_user to return test_user instance

Actions:
- open /logout
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- validate current page is /
- validate page shows element #welcome-message that says: 'Hi {}'.format(user.name)
- open /logout

### Test Case R3.3.1 - This page shows user balance. ###

Mocking:
- Mock backend.get_user to return test_user instance

Actions:
- open /logout
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- validate current page is /
- validate page shows element #balance that displays the value of test_user's balance.
- open /logout

### Test Case R3.4.1 - This page shows a logout link, pointing to /logout ###

Mocking:
- Mock backend.get_user to return test_user instance

Actions:
- open /logout
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- validate current page is /
- click element input[type="logout"]
- validate current page is /logout
- open /logout

### Test Case R3.5.1 - This page lists all available tickets. Information including the quantity of each ticket, the owner's email, and the price, for tickets that are not expired. ###

Mocking:
- Mock backend.get_user to return test_user intstance
- Mock backend.get_all_tickets to return test_tickets instance

Actions:
- open /logout
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- verify all tickets from test_tickets instance are listed
- validate that the quantity, owner's email, and the price are exactly as listed in test_tickets
- validate all tickets are not expired
- open /logout

### Test Case R3.6.1 - This page contains a form that a user can submit new tickets for sell. Fields: name, quantity, price, expiration date ###

Mocking:
- Mock backend.get_user to return test_user intstance

Action:
- open /logout
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- validate current page is /
- validate current page contains #sell-ticket header
- validate current page contains elements #sell-name, #sell-quantitiy, #sell-price, #sell-expiration-date
- open /logout

### Test Case R3.7.1 - This page contains a form that a user can buy new tickets. Fields: name, quantity ###

Mocking:
- Mock backend.get_user to return test_user intstance

Action:
- open /logout
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- validate current page is /
- validate current page contains #buy-ticket header
- validate current page contains elements #buy-name, #buy-quantitiy
- open /logout

### Test Case R3.8.1 - This page contains a form that a user can update existing tickets. Fields: name, quantity, price, expiration date ###

Mocking:
- Mock backend.get_user to return test_user intstance

Action:
- open /logout
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- validate current page is /
- validate current page contains #update-ticket header
- validate current page contains elements #update-name, #update-quantitiy, #update-price, #update-expiration-date
- open /logout



Mocking:
- Mock backend.get_user to return test_user intstance
- Mock backend.get_user to return test_ticket instance

Actions:
- open /logout
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- enter test_ticket's name into #sell-name element
- enter test_ticket's quantity into #sell-quantity element
- enter test_ticket's sell price into the #sell-price element
- enter test_ticket's expiration date into the #sell-expiration-date
- click element input[type="submit"]
- validate that the #sell-message element displays: "Ticket successfully placed in system."
- open /logout

### Test Case R3.10.1 - The ticket-buying form can be posted to /buy ###

Mocking:
- Mock backend.get_user to return test_user intstance
- Mock backend.get_user to return test_ticket instance

Actions:
- open /logout
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- enter test_ticket's name into #buy-name element
- enter test_ticket's quantity into #buy-quantity element
- click element input[type="submit"]
- validate that the #sell-message element displays: "Ticket(s) successfully purchased from system."
- open /logout

### Test Case R3.11.1 - The ticket-update form can be posted to /update ###

Mocking:
- Mock backend.get_user to return test_user intstance
- Mock backend.get_user to return test_ticket instance

Actions:
- open /logout
- open /login
- enter test_user's email into element #email
- enter test_user's password into element #password
- click element input[type="login"]
- enter test_ticket's name into #update-name element
- enter test_ticket's quantity into #update-quantity element
- enter test_ticket's sell price into the #update-price element
- enter test_ticket's expiration date into the #update-expiration-date
- click element input[type="submit"]
- validate that the #sell-message element displays: "Ticket successfully updated."
- open /logout
