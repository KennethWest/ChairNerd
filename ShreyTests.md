**R6.1 BUY POSITIVE**

This this test case shows how it would work if everything is submitted properly

`test_user = User(
     email='test_frontend@test.com',
     name='test_frontend',
     password=generate_password_hash('test_frontend')
 )`

`test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='test_ticket_yo',
    quantity=10,
    price=10,
    date='20200901'
)`

**Mocking:**
* Mock backend.get_user to return a test_user instance
* Mock backend.get_ticket to return a test_ticket instance

**Actions:**

* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user1's email into element #email
* enter test_user1's password into element #password
* click element input[type="submit"]
* open /
* enter test_ticket1's name into element #buy_name
* enter test_ticket1's quantity into element #buy_quantity
* click element #buy_submit
* validate that the #buy_message element shows successful
* open /logout (clean up)


**R6.2 BUY BUT NAME > 60 CHARACTERS**

The name of the ticket is no longer than 60 characters

`test_user = User(
     email='test_frontend@test.com',
     name='test_frontend',
     password=generate_password_hash('test_frontend')
 )`

`test_ticket = Ticket(
    owner='test_frontend@test.com',
    name=‘According to all known laws of aviation, there is no way a bee should be able to fly.’,
    quantity=10,
    price=10,
    date='20200901'
)`

**Mocking**
* [no need to mock backend]

**Actions**
* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* enter test_ticket's name into element #buy_name
* enter test_ticket's quantity into element #buy_quantity
* click element #buy_submit
* validate that the #buy_message element shows failure
* validate that the #buy_message element provides a message that the reason it failed was because the ticket name was over 60 characters
* open /
* validate current page is user home page
* open /logout (clean up)

**R6.3 - number too high**
The quantity of the tickets has to be more than 0, and less than or equal to 100.

`test_user = User(
     email='test_frontend@test.com',
     name='test_frontend',
     password=generate_password_hash('test_frontend')
 )`

`test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='test_ticket_yo',
    quantity=420,
    price=10,
    date='20200901'
)`

**Mocking**
* [no need to mock backend]

**Actions**

* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* enter test_ticket's name into element #buy_name
* enter test_ticket's quantity into element #buy_quantity
* click element #buy_submit
* validate that the #buy_message element shows failure
* validate that the #buy_message element provides a message that the reason it failed was because the ticket quantity was over 100
* open /
* validate current page is user home page
* open /logout (clean up)

**R6.3 - number too low**

`test_user = User(
     email='test_frontend@test.com',
     name='test_frontend',
     password=generate_password_hash('test_frontend')
 )`

`test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='test_ticket_yo',
    quantity=-1337,
    price=10,
    date='20200901'
)`

**Mocking**
* [no need to mock backend]

**Actions**

* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* enter test_ticket's name into element #buy_name
* enter test_ticket's quantity into element #buy_quantity
* click element #buy_submit
* validate that the #buy_message element shows failure
* validate that the #buy_message element provides a message that the reason it failed was because the ticket quantity was less than 0
* open /
* validate current page is user home page
* open /logout (clean up)


**R6.4 - The ticket name does not exist in the database**

The ticket name exists in the database and the quantity is more than the quantity requested to buy

`test_user = User(
     email='test_frontend@test.com',
     name='test_frontend',
     password=generate_password_hash('test_frontend')
 )`

`test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='test_ticket_yo',
    quantity=10,
    price=10,
    date='20200901'
)`

**Mocking:**
* Mock backend.get_user to return a test_user instance
* Mock backend.get_ticket to return a test_ticket instance

**Actions:**

* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* enter test_ticket's name into element #buy_name
* enter test_ticket's quantity into element #buy_quantity
* click element #buy_submit
* validate that the #buy_message element shows failure
* validate that the #buy_message element provides a message that the reason it failed was because the ticket name does not exist in the database
* open /
* validate current page is user home page
* open /logout (clean up)

**R6.4 - Quantity remaining is less than what is available in stock**

`test_user = User(
     email='test_frontend@test.com',
     name='test_frontend',
     password=generate_password_hash('test_frontend')
 )`

`test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='test_ticket_yo',
    quantity=10,
    price=10,
    date='20200901'
)`
**Mocking:**
* Mock backend.get_quantity to return an instance of how many there is currently remaining. 

**Actions:**
* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* enter test_ticket's name into element #buy_name
* enter test_ticket's quantity into element #buy_quantity
* click element #buy_submit
* validate that the #buy_message element shows failure
* validate that the #buy_message element provides a message that the reason it failed was because the quantity remaining is less than the quantity requested to buy
* open /
* validate current page is user home page
* open /logout (clean up)


**R6.5 User has more balance than the ticket price**

The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%)

`test_user = User(
     email='test_frontend@test.com',
     name='test_frontend',
     password=generate_password_hash('test_frontend')
 )`

`
test_ticket = Ticket(
    owner='test_frontend@test.com',
    name='test_ticket_yo',
    quantity=10,
    price=10,
    date='20200901'
)`


**Mocking:**

* Mock backend.get_user to return a test_user instance
* Mock backend.get_ticket to return a test_ticket instance

**Actions:**

* open /logout (to invalidate any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* enter test_ticket's name into element #buy_name
* enter test_ticket's quantity into element #buy_quantity
* click element #buy_submit
* validate that the #buy_message element shows failure
* validate that the #buy_message element provides a message that the reason it failed was because the user has less balance than the ticket price*quantity plus service fee (35%) + tax (5%) 
* open /
* validate current page is user home page
* open /logout (clean up)


**R7**
Logout will invalid the current session and redirect to the login page. After logout, the user shouldn't be able to access restricted pages.

`test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)`

**Mocking:**

* Mock backend.get_user


**Actions:**
* open /logout (to invalidate any logged-in sessions that may exist)
* Open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /
* open /logout (to actually start the logging out test)
* Open /register
* Validate current page is register
* Open /buy
* Validate current page is login
* Open /sell
* Validate current page is login
* Open /update
* Validate current page is login
* open /logout (clean up)