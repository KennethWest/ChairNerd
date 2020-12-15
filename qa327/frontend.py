from flask import render_template, request, session, redirect, url_for
import re
from datetime import datetime
from datetime import date
from qa327 import app
import qa327.backend as bn
from sqlalchemy import update
from qa327.models import Tickets, db, User

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
            if inner_function.__name__ == "login_get" or inner_function.__name__ == "register_get":
                return inner_function(None)
            return redirect('/login')

    # renaming the function name to work with multiple functions
    wrapped_inner.__name__ = inner_function.__name__

    # return the wrapped version of the inner_function:
    return wrapped_inner


# R4:
@app.route('/sell', methods=['POST'])
def sell_post():
    name = request.form.get('name')
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))
    expiry = request.form.get('expiry')
    email = session['logged_in']
    user = bn.get_user(email)
    tickets = bn.get_all_tickets()
    error_message = None

    # checking to see if the ticket name is alphanumeric only, ignoring spaces for now
    if name.replace(" ", "").isalnum() is False:
        error_message = "The name of the ticket has to be alphanumeric-only (and spaces allowed only if not the " \
                        "first or last character) "
    # if name is alphanumeric disregarding spaces, now just ensure there are no spaces in the first or last character
    elif name[0] == ' ' or name[len(name) - 1] == ' ':
        error_message = "Space allowed only if it is not the first or last character"
    elif len(name) > 60:
        error_message = "The name of the ticket can be no longer than 60 characters"
    elif quantity <= 0 or quantity > 100:
        error_message = "The quantity of tickets has to be more than 0 and less than or equal to 100"
    elif price < 10 or price > 100:
        error_message = "The ticket price has to be between $10 and $100 (inclusive)"
    else:
        try:  # checking to see if the inputted expiry date is of proper format
            expiry = datetime.strptime(expiry, "%Y%m%d").strftime('%Y%m%d')
        except ValueError as e:
            error_message = "Expiry date must be given in the format YYYYMMDD"
            return render_template('index.html', message=error_message, user=user, tickets=tickets)

        try:  # checking to see if the inputted expiry date is expired
            expiryTest = datetime.strptime(expiry, "%Y%m%d")
            today = date.today()
            if expiryTest.date() < today:
                error_message = "Invalid: Inputted expiry date is already expired"
        except ValueError as e:
            error_message = "ERROR"

    if error_message:
        return render_template('index.html', message=error_message, user=user, tickets=tickets)
    else:
        bn.create_ticket(name, quantity, price, expiry, email)
        tickets = bn.get_all_tickets()
        return render_template('index.html', message="Ticket successfully posted to sell", user=user, tickets=tickets)


'''
@app.route('/sell', methods=['GET'])
def sell_get():
    return render_template('index.html', message='')  # this should be sell.html
'''


@app.route('/buy', methods=['POST'])
def buy_post():
    name = request.form.get('name')
    quantity = int(request.form.get('quantity'))
    error_message = None
    message = None
    email = session['logged_in']
    user = bn.get_user(email)
    ticket = Tickets.query.filter(Tickets.name == name).first()

    # check to see that the name is alphanumeric only and there is no space that is the first or last character
    if len(name) > 60 or len(name) < 1 or name[0] == " " or name[-1] == " " or not (name.replace(" ", "").isalnum()):
        error_message = "Name format is incorrect"
    elif quantity < 1:
        error_message = "Not asking for any tickets"
    elif quantity > 100:
        error_message = "We cannot supply that many tickets at once"
    elif ticket is None:
        error_message = "No tickets with that name"
    elif user.balance <= (ticket.price * quantity) + (0.35 * (ticket.price * quantity)) + (
            0.05 * (ticket.price * quantity)):
        error_message = "Not enough user balance"
    elif ticket.quantity < quantity:
        error_message = "You are requesting more tickets than available for " + ticket.name + ". Please change your " \
                                                                                              "requested quantity. "
    else:
        # calculate the total price, the new balance based on that price and the new user balance
        totalPrice = (ticket.price * quantity) + (0.35 * (ticket.price * quantity)) + (0.05 * (ticket.price * quantity))
        newBalance = float(bn.get_user(email).balance) - totalPrice
        user.balance = newBalance
        # ticket deletes if the user requests the exact number of tickets available
        if ticket.quantity == quantity:
            db.session.delete(ticket)
        # tickets = bn.get_all_tickets()
        # return render_template('index.html', message=error_message, user=user, tickets=tickets, balance=newBalance)
        # otherwise quantity is updated
        else:
            quant = ticket.quantity - quantity
            ticket.quantity = quant
        db.session.commit()
        message = "Ticket successfully bought"

    if error_message is not None:
        return redirect(url_for('.profile', message=error_message))
    else:
        return redirect(url_for('.profile', message=message))


@app.route('/update', methods=['POST'])
def update_post():
    '''
    name = request.form.get('name')
    quantity = int(request.form.get('quantity'))
    error_message = None
    ticket = Tickets.query.filter(Tickets.name == name).first()
    email = session['logged_in']
    user = bn.get_user(email)
    tickets = bn.get_all_tickets()
    if ticket is None:
        error_message = "No tickets with that name"
    return render_template('index.html', message=error_message, user=user, tickets=tickets)
   '''

    # initialize variables
    error_message = None
    name = request.form.get('name-get')
    newName = request.form.get('name')
    getQuantity = request.form.get('quantity')
    if (getQuantity != ''):
        quantity = int(getQuantity)
    else:
        quantity = ''
    getPrice = request.form.get('price')
    if (getPrice != ''):
        price = float(getPrice)
    else:
        price = ''
    expiry = request.form.get('expiry')
    email = session['logged_in']
    userTicket = Tickets.query.filter(Tickets.name == name and Tickets.owner == email).first()
    user = bn.get_user(email)
    tickets = bn.get_all_tickets()

    if userTicket is None:
        error_message = "No tickets with that name"
        return render_template('index.html', message=error_message, user=user, tickets=tickets)

    # check name for spaces at the beginning and end
    if (newName != ''):
        if (newName[0] == ' ') or (newName[len(newName) - 1] == ' '):
            error_message = 'Error: Space allowed only if it is not the first or the last character'
            return render_template('index.html', message=error_message, user=user, tickets=tickets)

    # check length of name
    if (newName != ''):
        if len(newName) > 60:
            error_message = 'Error: Ticket name must not have more than 60 characters'
            return render_template('index.html', message=error_message, user=user, tickets=tickets)

    # check quantity of ticket
    if (quantity != ''):
        if 1 > quantity or quantity > 100:
            error_message = 'Error: Number of tickets must be between 1 and 100'
            return render_template('index.html', message=error_message, user=user, tickets=tickets)

    # check price of ticket
    if (price != ''):
        if 10 > price or price > 100:
            error_message = 'Error: Ticket price must be between 10 and 100 (inclusive)'
            return render_template('index.html', message=error_message, user=user, tickets=tickets)

    # check expiry date of ticket
    if (expiry != ''):

        try:  # checking to see if the inputted expiry date is of proper format
            expiry = datetime.strptime(expiry, "%Y%m%d").strftime('%Y%m%d')
        except ValueError as e:
            error_message = "Expiry date must be given in the format YYYYMMDD"
            return render_template('index.html', message=error_message, user=user, tickets=tickets)

        try:  # checking to see if the inputted expiry date is already expired
            expiryTest = datetime.strptime(expiry, "%Y%m%d")
            today = date.today()
            if expiryTest.date() < today:
                error_message = "Invalid: Inputted expiry date is already expired"
                return render_template('index.html', message=error_message, user=user, tickets=tickets)
        except ValueError as e:
            error_message = "ERROR"

    # check for special characters in the ticket name
    if (newName != ''):
        for char in newName:
            if char == ' ':
                continue
            if not char.isalnum():
                error_message = 'Error: The name of the ticket must be alphanumeric only'
                return render_template('index.html', message=error_message, user=user, tickets=tickets)

    if (newName != ''):
        userTicket.name = newName
    if (quantity != ''):
        userTicket.quantity = quantity
    if (price != ''):
        userTicket.price = price
    if (expiry != ''):
        userTicket.expiry = expiry
    db.session.commit()
    message = "Ticket successfully updated"
    return render_template('index.html', message=message, user=user, tickets=tickets)


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
        error_message = "Password not strong enough - must have minimum length 6, at least one upper case, at least " \
                        "one lower case, and at least one special character"

    elif len(name) >= 20 or len(name) < 3 or name[0] == " " or name[-1] == " " or not (name.replace(" ", "").isalnum()):
        error_message = "Name format is incorrect. User name has to be non-empty, longer than 2 characters and less " \
                        "than 20 characters, alphanumeric-only, and space allowed only if it is not the first or the " \
                        "last character"

    else:
        user = bn.get_user(email)
        if user:
            error_message = "This email has been ALREADY used"
        else:
            a = bn.register_user(email, name, password)
            if not a:
                error_message = "Failed to store user info."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return redirect(url_for('.login_get', message=error_message))
    else:
        return redirect('/')


@app.route('/login', methods=['GET'])
@authenticate
def login_get(user):
    if user:
        return redirect('/')
    try:
        message = request.args['message']
    except:
        message = "Please login"
    return render_template('login.html', message=message)


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
    if user != None:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between browser and the end server. Typically it is encrypted 
        and stored in the browser cookies. They will be past 
        along between every request the browser made to this services.
        Here we store the user object into the session, so we can tell
        if the client has already login in the following sessions.
        """
        tickets = bn.get_all_tickets()


        return redirect('/', code=303)
        ##return render_template('index.html', user=user, tickets=tickets)
    else:
        return render_template('login.html', message='email/password combination incorrect')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/register', methods=['GET'])
@authenticate
def register_get(user):
    if user:
        return redirect('/')
    return render_template('register.html', message='')


@app.route('/')
@authenticate
def profile(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals
    tickets = bn.get_all_tickets()
    try:
        message = request.args['message']
    except:
        message = ""
    return render_template('index.html', user=user, tickets=tickets, message=message)


@app.errorhandler(404)
def not_found_404(error):
    return render_template('404.html',
                           message='Uh Oh! Something is not quite right here, maybe you tried to access a page you do not have access to or one that has recently been deleted.'), 404
