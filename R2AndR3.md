# Ken's Test Cases R2 & R3 #

## Test Cases For R2: ##

### Test Case R2.1.1 - If a user is logged in, redirect back to the user profile page.###

Mocking:
-Mock backend.get_user to return a test_user instance

Actions:
-open /logout (to ensure there is no logged in user)
-open /login
-enter test_user's email into element #email
-enter test_user's password into element #password
-click element input[type="submit"]
-validate that current page contains #welcome-header element

### Test Case R2.1.2 - Otherwise, show the user the registration page. ###

Actions:
-open /logout (to ensure there is no logged in user)
-validate the current page contains #register-header element.

### Test Case R2.2.1 - The registration page shows a registration form requesting: email, user name, password, assword2. ###

Actions:
-open /logout (to ensure there is no logged in user)
-validate the current page contains #email element.
-validate the current page contains #user-name element.
-validate the current page contains #password element.
-validate the current page contains #password2 element.

### Test Case R2.3.1 - The registration form can be submitted as a POST request to the current URL (/register) ###

Actions:
-open /logout (to ensure there is no logged in user)
-