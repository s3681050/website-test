from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from . import db, write_to
from .models import User, ForumPost, Reply
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('userEmail')
        password = request.form.get('userPassword')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                log = f'Authentication-Login,\tSuccess,\t{email}'
                write_to(log)
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                log = f'Authentication-Login,\tFailure,\t{email},\tIncorrect password'
                write_to(log)
        else:
            log = f'Authentication-Login,\tFailure,\t{email},\tIncorrect username'
            write_to(log)

    return render_template("login.html", user=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    email = current_user.email
    if email:
        logout_user()
        log = f'Authentication-Logout,\tSuccess,\t{email},\tAccount logged out'
        write_to(log)
    return render_template("home.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Easy way to disable registration
    registration = True;

    if request.method == 'POST':
        email = request.form.get("userEmail")
        password = request.form.get('userPassword')
        passwordConfirm = request.form.get('userPasswordCheck')

        # Checks if we are allowed to register or not
        if registration == True:

# BEGIN VALIDATION
            # email length
            if len(email) < 4 or len(email) > 128:
                log = f'Account-Creation,\tFaliure,\t{email},\tEmail length'
                write_to(log)

            # user already exists
            elif User.query.filter_by(email=email.lower()).first():
                log = f'Account-Creation,\tFaliure,\t{email},\tEmail already exists'
                write_to(log)

            # enable this if we want to have a disallow list
            #elif DisallowedNames.query.filter_by(username=username.lower()).first():
            #    log = f'Account-Creation,\tFaliure,\t{username},\tDisallowed email'
            #    print(log)
            #    write_to(log)

            elif len(password) < 4 or len(password) > 64:
                log = f'Account-Creation,\tFaliure,\t{email},\tPassword length'
                write_to(log)

            elif password != passwordConfirm:
                log = f'Account-Creation,\tFaliure,\t{email},\tNo match passwords'
                write_to(log)
# End validation
            # create account
            else:
                new_user = User(email=email,
                                password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                log = f'Account-Creation,\tSuccess,\t{email}'
                write_to(log)
                login_user(new_user, remember=True)
                log = f'Authentication-Login,\tAutomatic,\t{email}'
                write_to(log)
                return redirect(url_for('views.home'))

        # Registration = false
        else:
            log = f'Account-Creation,\tUnavailable,\t{email},\tRegistration disabled'
            write_to(log)

    return render_template("sign_up.html", user=current_user)
# BUG REPORT
# After creating an account and logging in, submitting profile form can return NoneType error
# user=user sometimes does not load properly, indicated by a missing email under the profile pic
# ...To investigate.


@auth.route('/userPage')
def userOwnPage():
    return render_template("user_page.html", user=current_user)

@auth.route('/userSettings')
def userSettings():
    return render_template("user_settings.html", user=current_user)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        phoneNumber = request.form.get('phoneNumber')
        address = request.form.get('address')
        email = request.form.get('userEmail')
        education = request.form.get('education')
        country = request.form.get('country')
        region = request.form.get('region')
        experience = request.form.get('experience')
        additionalDetails = request.form.get('additionalDetails')
        displayPicture = request.form.get('displayPicture')

        # temporarily removed email changing
        user = User.query.filter_by(email=email).first()
        user.firstName = firstName
        user.lastName = lastName
        user.phoneNumber = phoneNumber
        user.address = address
        # user.email = email
        user.education = education
        user.country = country
        user.region = region
        user.experience = experience
        user.additionalDetails = additionalDetails
        # user.displayPicture = displayPicture

        db.session.commit()
        log = f'Account-Profile,\tUpdated,\t{email}'
        write_to(log)

    return render_template("profile.html", user=current_user, currentuser=current_user)

@auth.route('/forums')
def forums():
    return render_template("forums.html", user=current_user)

@auth.route('/chatbot')
def chatbot():
    return render_template("messenger.html", user=current_user)