from qa327.models import db, User, Tickets
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

"""
This file defines all backend logic that interacts with database and other services
"""


def get_user(email):
    """
    Get a user by a given email
    :param email: the email of the user
    :return: a user that has the matched email address
    """
    user = User.query.filter_by(email=email).first()
    return user


def login_user(email, password):
    """
    Check user authentication by comparing the password
    :param email: the email of the user
    :param password: the password input
    :return: the user if login succeeds
    """
    # if this returns a user, then the name already exists in database
    user = get_user(email)
    if not user or not check_password_hash(user.password, password):
        return None
    return user


def register_user(email, name, password):
    """
    Register the user to the database
    :param email: the email of the user
    :param name: the name of the user
    :param password: the password of user
    :return: an error message if there is any, or None if register succeeds
    """
    try:
        hashed_pw = generate_password_hash(password, method='sha256')
        # store the encrypted password rather than the plain password
        new_user = User(email=email, name=name, password=hashed_pw, balance=5000)
        db.session.add(new_user)
        db.session.commit()
        return True
    except:
        return False


def create_ticket(name, quantity, price, expiry, owner):
    #date = datetime.strptime(expiry, '%Y/%m/%d')
    new_ticket = Tickets(name=name, price=price, quantity=quantity, expiry=expiry, owner=owner)
    db.session.add(new_ticket)
    db.session.commit()
    return None


def get_all_tickets():
    return Tickets.query.all()

