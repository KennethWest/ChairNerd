  
from flask import render_template, request, session, redirect, url_for
import re
from datetime import datetime
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


@app.route('/sell', methods=['POST'])
def sell_post():
    name = request.form.get('name')
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))
    expiry = request.form.get('expiry')
    error_message = None
    email = session['logged_in']
    user = bn.get_user(email)
    bn.create_ticket(name, quantity, price, expiry, email)
    tickets = bn.get_all_tickets()
    error_message = "Ticket successfully posted to sell"
    return render_template('index.html', message=error_message, user=user, tickets=tickets)


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
    ticket = Tickets.query.filter(Tickets.name == name).first()
    email = session['logged_in']
    user = bn.get_user(email)
    tickets = bn.get_all_tickets()
    if ticket is None:
        error_message = "No tickets with that name"
    else:
        newBalance = float(bn.get_user(email).balance) - (float(ticket.price) * quantity)
        if ticket.quantity <= quantity:
            db.session.delete(ticket)
            user.balance = newBalance
            db.session.commit()
        # tickets = bn.get_all_tickets()
        # return render_template('index.html', message=error_message, user=user, tickets=tickets, balance=newBalance)
        else:
            quant = ticket.quantity - quantity
            ticket.quantity = quant
            user.balance = newBalance
            db.session.commit()
        error_message = "Ticket successfully bought"
    return render_template('index.html', message=error_message, user=user, tickets=tickets)


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

    name = request.form.get('name')
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))
    expiry = request.form.get('expiry')
    error_message = None
    userTicket = Tickets.query.filter(Tickets.name == name).first()
    email = session['logged_in']
    user = bn.get_user(email)
    tickets = bn.get_all_tickets()
    if userTicket is None:
        error_message = "No tickets with that name"
    else:
        #date = datetime.strptime(expiry, '%Y/%m/%d')
        #x = expiry.split('/')
        #date = datetime.datetime(x[0], x[1], x[2])
        userTicket.quantity = quantity
        userTicket.price = price
        userTicket.expiry = expiry
        db.session.commit()
        error_message = "Ticket successfully updated"
    return render_template('index.html', message=error_message, user=user, tickets=tickets)

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
    return render_template('index.html', user=user, tickets=tickets)

@app.errorhandler(404)
def not_found_404(error):
    return render_template('404.html',
                           message='Uh Oh! Something is not quite right here, maybe you tried to access a page you do not have access to or one that has recently been deleted.'), 404