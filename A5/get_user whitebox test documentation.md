# Whitebox Test Cases #
```python
def get_user(email):
    """
    Get a user by a given email
    :param email: the email of the user
    :return: a user that has the matched email address
    """
1   user = User.query.filter_by(email=email).first()
2   return user
```

Case 1
Inputs: email = "test_frontend_whitebox@test.com"
Line 1: user = the user object associated "test_frontend_whitebox@test.com"

Case 2
Inputs: email = "test_frontend_whitebox_wrong@test.com"
Line 1: user = None