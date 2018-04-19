"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from werkzeug.security import check_password_hash
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from forms import ProfileForm
from models import UserProfile
import datetime
import os


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

def date_created():
    now = datetime.datetime.now()
    return now.strftime("%c")


#return current date when the user sign up  
@app.route('/profile/', methods=["GET", "POST"])
@app.route('/profile/<userid>')
def profile():
    formfile = ProfileForm()
    
    if request.method == "POST":
        if formfile.validate_on_submit():
            firstname = formfile.firstname.data
            lastname = formfile.lastname.data
            gender = formfile.gender.data
            email = formfile.email.data
            location = formfile.location.data
            photo = formfile.photo.data
            bio = formfile.bio.data
            dateCreated = date_created()
            
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            newUser = UserProfile(firstname, lastname, gender, email, location, filename, bio, dateCreated)
            
            ##Get user information to be added to database
            db.session.add(newUser)
            db.session.commit()
            
            flash("Profile Successfully Created")
            return redirect(url_for('profile'))
    flash("Profile Unsuccessfully Created")
    return render_template('profile.html', form=formfile)
    
@app.route('/profiles')
def profiles():
    ListUsers = db.session.UserProfile.query.all()
    users = []
    for user in ListUsers:
        users.append(user)
    return render_template('profiles.html', users=users)
    
@app.route('/profile/<userid>')
def userProfile(userid):
    user = UserProfile.query.filter_by(id=userid).first()
    return render_template('profiles.html', user = user)


# @app.route("/login/", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
    
#     if request.method == "POST":
#         if form.validate_on_submit():
#             # Get the username and password values from the form.
#             username = form.username.data
#             password = form.password.data
#             # using your model, query database for a user based on the username
#             # and password submitted
#             user = UserProfile.query.filter_by(username = username).first()
#             # store the result of that query to a `user` variable so it can be
#             # passed to the login_user() method.
#             if user is not None and user.password:
#                 login_user(user)
#                 flash('Log in was successful', 'success')
#                 return redirect(url_for("profile"))
#             else:
#                 flash('Wrong password or username', 'Danger!')
#     return render_template('login.html', form=form)

# @app.route("/secure_page/")
# @login_required
# def secure_page():
#     return render_template('secure_page.html')
    
# @app.route("/logout/")
# def logout():
#     logout_user()
#     flash('Logout was successful')
#     return redirect('home')
    


# # user_loader callback. This callback is used to reload the user object from
# # the user ID stored in the session
# @login_manager.user_loader
# def load_user(id):
#     return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
