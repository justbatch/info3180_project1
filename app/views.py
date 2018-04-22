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

def date_created():
    now = datetime.datetime.now()
    return now.strftime("%c")

#return current date when the user sign up  
 # after here I should have

@app.route('/profile/<userid>') 
@app.route('/profile', methods=["GET", "POST"])
def profile(userid = None): # I tried that too and even did this in the ridrect
    formfile = ProfileForm()
    if userid:
        # this is working now. test it 
        # when the form is submitted and the user gets created, it redirects to profile/userid 
        return str(userid)
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
            
            newUser = UserProfile(firstname, lastname, email, location, gender, bio, photo, dateCreated)
            ##Get user information to be added to database
            db.session.add(newUser)
            db.session.commit()
            
            ##Get new users or users id
            userid = newUser.get_id()
            
            ##worked now I was trying a if statement in my profile that after it is submitted it will bring up a display
            
            #sorry about started to look at something
            # where do you want to navigate to after the user is created? 
            #should be the same page but along with the new userid in the url, basically should be routed to the new user profile after submission
            flash("Profile Created", "Success")
            return  redirect('/profile/'+str(userid))
            
    # flash_errors(formFile)        
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
    listUsers = db.session.query(UserProfile).all()
    # userphoto = get_uploaded_images()
    users = []
    users.append(listUsers)
    
    return render_template('profiles.html', users=users)

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
