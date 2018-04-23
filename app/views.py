"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from werkzeug.security import check_password_hash
from flask import render_template, request, redirect, url_for, flash, session, abort
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

#return current date when the user sign up 
def date_created():
    now = datetime.datetime.now()
    return now.strftime("%c")

@app.route('/profile', methods=["GET", "POST"])
def profile():
    formfile = ProfileForm()
   
    if request.method == "POST":
        if formfile.validate_on_submit():
            
            firstname = formfile.firstname.data
            lastname = formfile.lastname.data
            gender = formfile.gender.data
            email = formfile.email.data
            location = formfile.location.data
            img = formfile.img.data
            bio = formfile.bio.data
            dateCreated = date_created()
            
            photo = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], photo))
            
            #new user data from form adding to the database paramaters
            newUser = UserProfile(firstname, lastname, email, location, gender, bio, photo, dateCreated)
            ##Get user information to be added to database
            db.session.add(newUser)
            db.session.commit()
            
            flash("Profile Created", "Success")
            return  redirect(url_for('profiles'))
    # flash_errors(formfile)        
    return render_template('profile.html', form=formfile)

def get_uploaded_images():
    images = []
    for files in os.walk(app.config['UPLOAD_FOLDER']):
        for file in files:
            images.append(file)
    
    images.sort()
    del images[0]
    return images
    
@app.route('/profiles')
def profiles():
    # listUsers = UserProfile.query.all()
    listUsers = db.session.query(UserProfile.lastname).all()
    # userphoto = get_uploaded_images()
    return render_template('profiles.html', users=listUsers)

@app.route('/profile/<userid>')
def userid(userid):
    if userid is None:
        error = "User does not exist"
        return render_template('home.html', error=error)
    userid = db.session.query(UserProfile.lastname).order_b(id=userid)
    return  render_template('userid.html', userid=userid)
    
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
