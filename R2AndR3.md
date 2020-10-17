# Ken's Test Cases R2 & R3 #

## Test Cases For R2: ##

### Test Case R2.1.1 - If a user is logged in, redirect back to the user profile page ###

Mocking:
-Mock backend.get_user to return a test_user instance

Actions:
-open /logout (to ensure there is no logged in user)
-open /login
-enter test_user's email into element #email
-enter test_user's password into element #password
-click element input[type="submit"]
-validate that current page is /

### Test Case R2.1.2 - Otherwise, show the user the registration page ###

Actions:
-open /logout (to ensure there is no logged in user)
-validate the current page is /register.

### Test Case R2.2.1 - The registration page shows a registration form requesting: email, user name, password, assword2 ###

Actions:
-open /logout (to ensure there is no logged in user)
-open /register
-validate the current page contains #email element.
-validate the current page contains #user-name element.
-validate the current page contains #password element.
-validate the current page contains #password2 element.

### Test Case R2.3.1 - The registration form can be submitted as a POST request to the current URL (/register) ###

Actions:
-open /logout (to ensure there is no logged in user)
-open /register
-enter create_user's email into element #email
-enter create_user's user-name into element #user-name
-enter create_user's password into element #password
-enter create_user's password again into element #password2
-click element input[type="submit"]
-validate that #register_message element shows successful
-validate that current page is now /login

### Test Case R2.4.1 - Email, password, password2 all satisfy the same requirements defined in R1 - Negative ###

Actions:
-open /logout
-open /register
-enter one of the following bellow to not meet the specifications outlined in R1:
-enter create_user's email into element #email
-enter create_user's password into element #password
-enter create_user's password2 into element #password2
-validate that #error_message element shows details on invalid input

### Test Case R2.4.2 - Email, password, password2 all satisfy the same requirements defined in R1 - Postitive ###

Actions:
-open /logout
-open /register
-enter all of the following bellow such that they meet the specifications outlined in R1:
-enter create_user's email into element #email
-enter create_user's password into element #password
-enter create_user's password2 into element #password2
-validate that element #green_check is displayed next to each input box

### Test Case R2.5.1 - Password and password2 have to be exactly the same - Negative ###

Actions:
-open /logout
-open /register
-enter create_user's password into element #password
-enter create_user's password into element #password2 such that it is not the same as what is in element #password
-validate that element #red_ex is next to the password boxes
-validate that element #error-message explains password mismatch

### Test Case R2.5.2 - Password and password2 have to be exactly the same - Positive ###

Actions:
-open /logout
-open /register
-enter create_user's password into element #password
-enter create_user's password into element #password2
-validate that element #green_check is displayed next to each input box

### Test Case R2.6.1 - Username has to be non-empty, alphanumeric-only, and space allowed only if its not the first or last character. Username has to be longer than 2 characters and less than 20 - Negative ###

Actions:
-open /logout
-open /register
-enter enter create_user's user-name such that it does not meet at least following specifications:
	-User-name must not be empty
	-User-name must be alphanumeric-only
	-User-name may contain a space only if its not the first an last character
	-User-name must be longer than 2 characters and less than 20.
-validate that the element #red_ex is displayed next to the username input box
-validate that the element #error-message explains invalid user-name entry

### Test Case R2.6.2 - Username has to be non-empty, alphanumeric-only, and space allowed only if its not the first or last character. Username has to be longer than 2 characters and less than 20 - Positive ###

Actions:
-open /logout
-open /register
-enter create_user's user-name such that it does meet all of the following specifications:
	-User-name must not be empty
	-User-name must be alphanumeric-only
	-User-name may contain a space only if its not the first an last character
	-User-name must be longer than 2 characters and less than 20.
-validate that the element #green_check is displayed next to the username input box


### Test Case R2.7.1 - For any formatting errors, redirect back to /login and show message '{} format is incorrect.'.format(the_corresponding_attribute) ###

Actions:
-open /logout
-open /register
-enter at least one of the follow in a way such that it does not mean the requirments tests in R2.4.1 - R2.6.2:
-enter create_user's email into the element #email
-enter create_user's user-name into the element #user-name
-enter create_user's password into the element #password
-enter create_user's password into the element #password2
-click element input[type="submit"]
-validate page redirects to /login
-validate #error-message element displays: '{} format is incorrect.'.format(the_corresponding_attribute), where the_corresponding_attribute is either email, password, or user-name.

### Test Case R2.8.1 - If the email already exists, show message 'this email has been ALREADY used' ###

Mocking:
-Mock backend.get_user to return a test_user instance

Actions:
-open /logout
-open /register
-enter test_user's email into the element #email
-validate #red_ex element is displayed next to element #email
-validate #error-message element displays: "This email is already in use. Please either login or enter another email."

### Test Case R2.9.1 - If no error regarding the inputs following the rules above, create a new user, set the balance to 5000, and go back to the /login page ###

Mocking:
-Mock backend.get_user to return test_user instance

Actions:
-open /logout
-open /register
-enter test_user's email into element #email
-enter test_user's user-name into element #user-name
-enter test_user's password into element #password
-enter test_user's password again into element #password2
-click element input[type="submit"]
-validate that #register_message element shows successful
-validate that current page is now /login
-enter test_user's email into element #email
-enter test_user's password into element #password
-click element input[type="login"]
-validate that current page is /
-validate that test_user balance is 5000.
-open /logout