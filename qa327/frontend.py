from flask import render_template, request, session, redirect
from qa327 import app
import qa327.backend as bn
from sqlalchemy import update

from qa327.models import Tickets

"""
This file defines the front-end part of the service.
It elaborates how the services should handle different
http requests from the client (browser) through templating.
The html templates are stored in the 'templates' folder. 
"""


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

    elif len(email) < 1:
        error_message = "Email format error"

    elif len(password) < 1:
        error_message = "Password not strong enough"
    else:
        user = bn.get_user(email)
        if user:
            error_message = "User exists"
        elif not bn.register_user(email, name, password, password2):
            error_message = "Failed to store user info."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
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
        return render_template('login.html', message='login failed')


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
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


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
