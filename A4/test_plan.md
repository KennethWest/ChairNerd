# Test Plan

## Test Structure

Our test cases will be located within a directory in our repository called /qa327_test. Inside, there will be two folders which contain frontend and backend/integration test cases respectively.

The order of our testing will go as follows:

1. Frontend
2. Backend/Integration

We want to test the frontend first since we have the ability to mock a backend. With a functioning frontend, we can easily observe backend actions.

## Techniques, Tools and Budget Management

A technique we will use to run our test cases is regression testing, and we will utilize specifically priority testing to test the functions that are most vital to our program and most affected by user inputs with high failure rates. E.g. if there is a high fault rate within login service, we would run only the test cases that concern the login process.

To run our automated tests, we will use GitHub actions, Pytest and the Selenium API. Such small testing phases will be carried out locally on each individual function, then unit and then finally on the system as a whole. Cloud testing will only occur after each level of implementation (frontend, backend, integration) has been completed and merged to our master branch. This is so we save CI resources for the larger phases of testing, instead of wasting them on small testing phases.

Using this method, we will be running a cloud environment test just before each major release. After each cloud environment test has completed, we will generate a file which summarizes all the results, and keep them stored in the /tests/logs located in our repository. By leveraging this, we can keep track of any recurring errors and identify areas of high failure which will increase efficiency in the debugging process.

## Points of contact upon failed test

In the event of a failed test from R1-R8, the following specified individuals should be made aware of the failure:

R1 - Daniel Oh

R2 - Shreyansh Anand

R3 - Lia Sanfilippo

R4 - Lia Sanfilippo & Kenneth West

R5 - Daniel Oh

R6 - Shreyansh Anand

R7 - Kenneth West

R8 - Kenneth West

Any specifications labeled with a TBD have not been implemented, and thus does not have any point for contact.