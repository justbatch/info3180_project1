from . import db


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    gender = db.Column(db.String(8))
    email = db.Column(db.String(80))
    location = db.Column(db.String(80))
    photo = db.column(db.String(80))
    bio = db.Column(db.String(255))
    created_on = db.Column(db.String(80))

    def __init__(self, firstname, lastname, email, location, gender, bio, photo, created_on):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.gender = gender
        self.bio = bio
        self.photo = photo
        self.created_on = created_on

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
