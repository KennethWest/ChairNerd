R4 and R5 Test Cases

**Test Case R4.1.1 - /sell[POST] Check if the selling actions succeed when the ticket name is alphanumeric-only**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put ticket name into element #ticketName
- use isalnum() method on ticketName to validate that it contains all alphanumeric characters
- validate that the #sell_message element shows successful
- open /logout (clean up)

**Test Case R4.1.2 - /sell[POST] Check if the selling actions fail when the ticket names contain special characters**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put ticket name into element #ticketName
- use isalnum() method on ticketName to validate that it does not contain only alphanumeric characters
- validate that the #sell_message element shows “Error: The name of the ticket must be alphanumeric only”
- open /logout (clean up)

**Test Case R4.1.3 - /sell[POST] Check if the selling actions succeed when the ticket names contain a space that is not the first or last character** 

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put ticket name into element #ticketName
- use indexing at [0] and at [length of ticket name-1] to get the first and last characters of the ticket name
- use isspace() method to check if there is a space in either characters 
- validate that the #sell_message element shows successful
- open /logout (clean up)

**Test Case R4.1.4 - /sell[POST] Check if the selling actions fail when the ticket names contain a space as the first character, the last character, or both**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put ticket name into element #ticketName
- use indexing at [0] and at [length of ticket name-1] to get the first and last characters of the ticket name
- use isspace() method to check if there is a space in either characters 
- validate that the #sell_message element shows “Error: Space allowed only if it is not the first or the last character” 
- open /logout (clean up)

**Test Case R4.2.1 - /sell[POST] Check if the selling actions succeed when the ticket name is less than 60 characters (but not empty) or exactly 60 characters**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put ticket name into element #ticketName
- use len() to get the value of the length of ticketName
- validate that the value is less than or equal to 60, and greater than zero
- validate that the #sell_message element shows successful 
- open /logout (clean up)

**Test Case R4.2.2 - /sell[POST] Check if the selling actions fail when the ticket name is more than 60 characters, or zero characters (empty)**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put ticket name into element #ticketName
- use len() to get the value of the length of ticketName
- validate that the value is not less than or equal to 60 characters, or is zero
- validate that the #sell_message element shows “Error: Ticket name must not have more than 60 characters, and cannot be empty”
- open /logout (clean up)

**Test Case R4.3.1 - /sell[POST] Check if the selling actions succeed when the quantity of the tickets is between 1 and 100 (inclusive)**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put the quantity of tickets into element #ticketNum
- validate that the value of ticketNum is between 1 and 100 (inclusive)
- validate that the #sell_message element shows successful
- open /logout (clean up)


**Test Case R4.3.2 - /sell[POST] Check if the selling actions fail when the quantity of tickets is over 100, is zero, or is negative**

Mocking: N/A 

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put the quantity of tickets into element #ticketNum
- validate that the value of ticketNum is not between 1 and 100 (inclusive)
- validate that the #sell_message element shows “Error: Number of tickets must be between 1 and 100”
- open /logout (clean up)


**Test Case R4.4.1 - /sell[POST] Check if the selling actions succeed when the price of a ticket is between 10 and 100 (inclusive)**

Mocking: N/A 

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put the price of the ticket into element #ticketPrice
- validate that the value of ticketPrice is between 10 and 100 (inclusive)
- validate that the #sell_message element shows successful
- open /logout (clean up)

**Test Case R4.4.2 - /sell[POST] Check if the selling actions fail when the price of a ticket is less than 10, or  over 100**

Mocking: N/A 

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put the price of the ticket into element #ticketPrice
- validate that the value of ticketPrice is less than 10 or greater than 100 
- validate that the #sell_message element shows “Error: Ticket price must be between 10 and 100 (inclusive)
- open /logout (clean up)

**Test Case R4.5.1  - /sell[POST] Check if the selling actions succeed when the date is in the format YYYYMMDD**

Mocking: N/A 

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put the date entered into element #ticketDate
- take the first four integers of date and assume this is the year, the next two integers to assume are the month, and the last two integers to assume are day 
- import datetime and use this to validate that ticketDate is in the proper format
- validate that the #sell_message element shows successful 
- open /logout (clean up)

**Test Case R4.5.2  - /sell[POST] Check if the selling actions fail when the date is in any other format (YYMMDD, YYYYMMD, YYYYDDMM, MMDDYYYY, DDMMYYYY etc)**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- put the date entered into element #ticketDate
- take the first four integers of date and assume this is the year, the next two integers to assume are the month, and the last two integers to assume are day 
- import datetime and use this to validate that ticketDate is not in the proper format
- validate that the #sell_message element shows “Error: Date must be given in the format YYYYMMDD”
- open /logout (clean up)

**Test Case R4.6.1 - /sell[POST] Check that for any and every error, the user is redirected back to the user home page**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- validate that you are redirected back to /
- open /logout (clean up)

**Test Case R4.6.2 - /sell[POST] Check that for any and every error, an appropriate error message is shown**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /sell 
- validate that the #sell_message element shows the name of the error
- open /logout (clean up)

**Test Case R4.7.1 - /sell[POST] The added new ticket information will be posted on the user profile page**

Mocking: 
- Mock backend.get_user to return a test_user instance
- Mock backend.get_ticket to return a test_ticket instance

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login 
- enter test_user's e-mail into element #email 
- enter test_user's password into element #password
- click element input[type="submit"] 
- open / 
- enter test_ticket's name into element #ticketName 
- enter test_ticket's quantity into element #ticketNum
- enter test_ticket's price into element #ticketPrice
- enter test_ticket's date into element #ticketDate
- click element #sell_submit
- validate that the #update_message element shows successful 
- validate that / is updated with the new information
- open /logout (clean up)


**Test Case R5.1.1 - /update[POST] Check if the updating actions succeed when the ticket name is alphanumeric-only**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update
- put ticket name into element #ticketName
- use isalnum() method on ticketName to validate that it contains all alphanumeric characters
- validate that the #update_message element shows successful
- open /logout (clean up)

**Test Case R5.1.2 - /update[POST] Check if the updating actions fail when the ticket names contain special characters**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update
- put ticket name into element #ticketName
- use isalnum() method on ticketName to validate that it does not contain only alphanumeric characters
- validate that the #update_message element shows “Error: The name of the ticket must be alphanumeric only”
- open /logout (clean up)

**Test Case R5.1.3 - /update[POST] Check if the updating actions succeed when the ticket names contain a space that is not the first or last character**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update
- put ticket name into element #ticketName
- use indexing at [0] and at [length of ticket name-1] to get the first and last characters of the ticket name
- use isspace() method to check if there is a space in either characters 
- validate that the #update_message element shows successful
- open /logout (clean up)

**Test Case R5.1.4 - /update[POST] Check if the updating actions fail when the ticket names contain a space as the first character, the last character, or both**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update 
- put ticket name into element #ticketName
- use indexing at [0] and at [length of ticket name-1] to get the first and last characters of the ticket name
- use isspace() method to check if there is a space in either characters 
- validate that the #update_message element shows “Error: Space allowed only if it is not the first or the last character” 
- open /logout (clean up)

**Test Case R5.2.1 - /update[POST] Check if the updating actions succeed when the ticket name is less than 60 characters (but not empty) or exactly 60 characters**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update 
- put ticket name into element #ticketName
- use len() to get the value of the length of ticketName
- validate that the value is less than or equal to 60, and greater than zero
- validate that the #update _message element shows successful 
- open /logout (clean up)


**Test Case R5.2.2 - /update[POST] Check if the updating actions fail when the ticket name is more than 60 characters, or zero characters (empty)**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update  
- put ticket name into element #ticketName
- use len() to get the value of the length of ticketName
- validate that the value is not less than or equal to 60 characters, or is zero
- validate that the #update _message element shows “Error: Ticket name must not have more than 60 characters, and cannot be empty”
- open /logout (clean up)

**Test Case R5.3.1 - /update[POST] Check if the selling actions succeed when the quantity of the tickets is between 1 and 100 (inclusive)**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update 
- put the quantity of tickets into element #ticketNum
- validate that the value of ticketNum is between 1 and 100 (inclusive)
- validate that the #update_message element shows successful
- open /logout (clean up)

**Test Case R5.3.2 - /update[POST] Check if the selling actions fail when the quantity of tickets is over 100, is zero, or is negative**

Mocking: N/A 

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update  
- put the quantity of tickets into element #ticketNum
- validate that the value of ticketNum is not between 1 and 100 (inclusive)
- validate that the #update_message element shows “Error: Number of tickets must be between 1 and 100”
- open /logout (clean up)


**Test Case R5.4.1 - /update[POST] Check if the selling actions succeed when the price of a ticket is between 10 and 100 (inclusive)**

Mocking: N/A 

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update 
- put the price of the ticket into element #ticketPrice
- validate that the value of ticketPrice is between 10 and 100 (inclusive)
- validate that the #update_message element shows successful
- open /logout (clean up)

**Test Case R5.4.2 - /update[POST] Check if the selling actions fail when the price of a ticket is less than 10, or is over 100**

Mocking: N/A 

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update 
- put the price of the ticket into element #ticketPrice
- validate that the value of ticketPrice is less than 10 or greater than 100 
- validate that the #update_message element shows “Error: Ticket price must be between 10 and 100 (inclusive)”
- open /logout (clean up)

**Test Case R5.5.1  - /update[POST] Check if the selling actions succeed when the date is in the format YYYYMMDD**

Mocking: N/A 

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update 
- put the date entered into element #date
- take the first four integers of date and assume this is the year, the next two integers to assume are the month, and the last two integers to assume are day 
- import datetime and use this to validate that the date is in the proper format
- validate that the #update_message element shows successful 
- open /logout (clean up)

**Test Case R5.5.2  - /update[POST] Check if the selling actions fail when the date is in any other format (YYMMDD, YYYYMMD, YYYYDDMM, MMDDYYYY, DDMMYYYY etc)**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update 
- put the date entered into element #date
- take the first four integers of date and assume this is the year, the next two integers to assume are the month, and the last two integers to assume are day 
- import datetime and use this to validate that the date is not in the proper format
- validate that the #update_message element shows “Error: Date must be given in the format YYYYMMDD”
- open /logout (clean up)

**Test Case R5.6.1  - /update[POST] Check if the updating actions succeed if the ticket name is found in the database**

Mocking: 
- Mock backend.get_user to return a test_user instance
- Mock backend.get_ticket to return a test_ticket instance

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist)
- open /login 
- enter test_user's e-mail into element #email 
- enter test_user's password into element #password
- click element input[type="submit"] 
- open / 
- enter test_ticket's name into element #update_name 
- enter test_ticket's quantity into element #update_quantity 
- click element #update_submit
- validate that the #update_message element shows successful 
- open /logout (clean up)

**Test Case R5.6.2  - /update[POST] Check if the updating actions fail if the ticket name is not found in the database**

Mocking:
- Mock backend.get_user to return a test_user instance
- Mock backend.get_ticket to return a test_ticket instance

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /login 
- enter test_user's email into element #email 
- enter test_user's password into element #password 
- click element input[type="submit"] 
- open / 
- enter the nonexistent ticket name into element #update_name 
- enter test_ticket's quantity into element #update_quantity 
- click element #buy_submit 
- validate that the #buy_message element shows "ticket does not exist" 
- open /logout (clean up)

**Test Case R5.7.1 - /update[POST] Check that for any and every error, the user is redirected back to the user home page**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /login 
- validate that the website is redirected to the user home page 
- open /logout (clean up) 

**Test Case R5.7.2 - /update[POST] Check that for any and every error, an appropriate error message is shown**

Mocking: N/A

Actions: 
- open /logout (to invalidate any logged-in sessions that may exist) 
- open /update
- validate that an appropriate error message is shown
- open /logout (clean up) 


