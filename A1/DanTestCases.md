## Daniel Oh R1 Specifications and Test Cases
### Note: before running a test case, always open /logout to remove any possible logged-in sessions

**Test case R1.1.1 - If the user hasn't logged in, show the login page**

Mocking:

- mock backend.get_user to return a test_user instance

Actions:

- reopen the whole site
- validate that the user is taken to /login


**Test case R1.1.2 - the login page has a message that by default says 'please login'**

Mocking:

- mock backend.get_user to return a test_user instance

Actions:

- open /login
- validate that the user is shown a message that says 'please login'


New Test Data:
``
test_user = User(
    email='test_frontend@test.com',
    name='test frontend',
    password='Test_frontend#'
)
``

**Test case R1.1.3 - If the user has logged in, redirect to the user profile page**

Mocking:

- mock backend.get_user to return a test_user instance

Actions:

- open /login
- enter tester's email into the email element
- enter tester's password into the password element
- click the log in button
- validate that you are on tester's profile page
- reload the root page
- open /login
- validate that you are on tester's profile page


**Test case R1.1.4 - The login page provides a login form which requests two fields: email and password**

Mocking:

- mock backend.get_user to return a test_user instance

Actions:

- open /login
- validate that there are two elements for email and password in which text can be entered


**Test case R1.2.1 - The login form can be submitted as a POST request to the current URL (/login)**

Mocking:

- mock backend.get_user to return a test_user instance

Actions:

- open /login
- enter tester's email into the email element
- enter tester's password into the password element
- click the log in button (post request)
- validate that you are on tester's profile page


**Test case R1.2.2 - Email and password both cannot be empty**

Mocking:

- mock backend.get_user to return a test_user instance

Actions:

- open /login
- click the 'sign in' button
- validate that we are still on /login


**Test case R1.2.3 - Email has to follow addr-spec defined in RFC 5322**
**Additional test case R1.2.5 - For any formatting errors, render the login page and show the message 'email/password format is incorrect.'**

Mocking:

- mock backend.get_user to return a test_user instance

Actions:

- open /login
- enter many different email formats that does not follow RFC 5322 standards (https://en.wikipedia.org/wiki/Email_address)
- validate that they make the email field display an 'invalid email' error message
- validate that the sign in button log you in
- enter in test@example.com
- validate that the error message is not present


**Test case R1.2.4 - Password has to meet the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character**
**Additional test case R1.2.5 - For any formatting errors, render the login page and show the message 'email/password format is incorrect.'**

Mocking:

- mock backend.get_user to return a test_user instance

Actions:

- open /login
- enter in a password for each of the following requirements:
    - 5 character length
    - no upper case letters
    - no lower case letters
    - no special characters
- validate that each of these attempts gives an error message
- validate that for each of these attempts the sign in button log you in
- enter in one password that meets the following requirements
    - minimum length 6
    - at least one upper case
    - at least one lower case
    - at least one special character
- validate that this does not give an error message


**Test case R1.2.6 - If email/password are correct, redirect to /. Otherwise, redirect to /login and show message 'email/password combination incorrect'**

Mocking:

- mock backend.get_user to return a test_user instance

Actions:

- open /login
- enter in 'wrong.email@example.com' into the email element and 'Wrong_Password' into the password element
- click the sign in button
- validate that you are redirected back to /login and an 'email/password combination incorrect' is shown
- reload /login
- enter tester's email ('testuser@example.com') and password ('Tester_pass') into their respective elements
- click the sign in button
- validate that you are redirected to /


**Test case R8 - For any other requests except /login, /register, /, /login, /buy, /sell, the system should return a 404 error**

Mocking:

- mock a backend to send post and get requests

Actions:

- use the mock backend to send post and get requests to any route not defined in the specification
- validate that all attempts return the proper 404 error
- try opening pages that are not /login, /register and /
- validate that all attempts display a 404 page