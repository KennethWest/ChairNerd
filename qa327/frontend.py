from flask import render_template, request, session, redirect
from qa327 import app
import qa327.backend as bn
import random
import re
from sqlalchemy import update
from qa327.models import Tickets


"""
This file defines the front-end part of the service.
It elaborates how the services should handle different
http requests from the client (browser) through templating.
The html templates are stored in the 'templates' folder. 
"""

def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object

    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.

    To wrap a function, we can put a decoration on that function.
    Example:

    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            user = bn.get_user(email)
            if user:
                # if the user exists, call the inner_function
                # with user as parameter
                return inner_function(user)
        else:
            # else, redirect to the login page
            if inner_function.__name__ == "login_get":
                return inner_function(None)
            return redirect('/login')

    # renaming the function name to work with multiple functions
    wrapped_inner.__name__ = inner_function.__name__

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/sell', methods=['POST'])
def sell_post():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    expiry = request.form.get('expiry')
    error_message = None
    owner = session['logged_in']
    bn.create_ticket(name, quantity, price, expiry, owner)
    return redirect('/')


@app.route('/sell', methods=['GET'])
def sell_get():
    return render_template('register.html', message='')  # this should be sell.html


@app.route('/buy', methods=['POST'])
def buy_post():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    error_message = None
    ticket = Tickets.query.filter(Tickets.name == name).first()
    email = session['logged_in']
    newBalance = bn.get_user(email).balance - ticket.price * quantity
    if ticket.quantity < quantity:
        Tickets.delete(ticket)
    else:
        quant = ticket.quantity - quantity
        update(ticket).values(quantity=quant)
        update(bn.get_user(email)).values(balance=newBalance)

    return redirect('/')


@app.route('/update', methods=['POST'])
def update_post():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    expiry = request.form.get('expiry')
    email = session['logged_in']
    error_message = None
    update(Tickets).where(Tickets.owner == email).values(name=name, quantity=quantity, price=price, expiry=expiry)
    return redirect('/')


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"

    elif not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        error_message = "Email format is incorrect"

    elif not re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,}$", password):
        error_message = "Password not strong enough"

    elif len(name) > 20 or len(name) < 3 or name[0] == " " or name[-1] == " " or not (name.replace(" ", "").isalnum()):
        error_message = "Name format is incorrect."

    else:
        user = bn.get_user(email)
        if user:
            error_message = "this email has been ALREADY used"
        elif not bn.register_user(email, name, password):
            error_message = "Failed to store user info."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('login.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/login', methods=['GET'])
@authenticate
def login_get(user):
    if user:
        return redirect('/')
    return render_template('login.html', message='Please login')


# This code runs when the user clicks the login button on the login page
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    # check if email is valid
    email_invalid = False
    if not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        email_invalid = True

    # check if password is valid
    password_invalid = False
    if not re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,}$", password):
        password_invalid = True

    # send the correct error message if either email_invalid or password_invalid are True
    if email_invalid and password_invalid:
        return render_template('login.html', message='email/password format is incorrect')
    elif email_invalid:
        return render_template('login.html', message='email format is incorrect')
    elif password_invalid:
        return render_template('login.html', message='password format is incorrect')

    user = bn.login_user(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between browser and the end server. Typically it is encrypted 
        and stored in the browser cookies. They will be past 
        along between every request the browser made to this services.

        Here we store the user object into the session, so we can tell
        if the client has already login in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='email/password combination incorrect')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object

    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.

    To wrap a function, we can put a decoration on that function.
    Example:

    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            user = bn.get_user(email)
            if user:
                # if the user exists, call the inner_function
                # with user as parameter
                return inner_function(user)
        else:
            # else, redirect to the login page
            # print(wrapped_inner().__name__)
            if inner_function.__name__ == "register_get":
                return render_template('register.html', message='')
            return redirect('/login')

    # the only way I could get this decorator to work
    wrapped_inner.__name__ = str(random.random())
    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/register', methods=['GET'])
@authenticate
def register_get(user):
    # templates are stored in the templates folder
    return redirect('/')


@app.route('/')
@authenticate
def profile(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals
    tickets = bn.get_all_tickets()
    return render_template('index.html', user=user, tickets=tickets)
  
  
@app.errorhandler(404)
def not_found_404(error):
    return render_template('404.html', message='Uh Oh! Something is not quite right here, maybe you tried to access a page you do not have access to or one that has recently been deleted.'), 404

