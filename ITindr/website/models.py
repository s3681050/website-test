from . import db 
from flask_login import UserMixin
from sqlalchemy import func

class User(db.Model, UserMixin):
    groupId = db.Column(db.Integer)
    firstName = db.Column(db.String(32))
    lastName = db.Column(db.String(32))
    address = db.Column(db.String(256))
    email = db.Column(db.String(128), primary_key=True, unique=True)
    password = db.Column(db.String(256))
    education = db.Column(db.String(128))
    country = db.Column(db.String(32))
    region = db.Column(db.String(32))
    experience = db.Column(db.String(256))
    additionalDetails = db.Column(db.String(256))
    phoneNumber = db.Column(db.Integer)
    displayPicture = db.Column(db.String(1024))

    def get_id(self):
        return (self.email)
    # Jake: add phonenumber


# Trying to create a space to store all of the forum posts in
class ForumPost(db.Model):
    forumID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Integer, db.ForeignKey('user.email'))
    userFistName = db.Column(db.Integer, db.ForeignKey('user.firstName'))
    userLastName = db.Column(db.Integer, db.ForeignKey('user.lastName'))
    # Im unser weather this is how we will store the information for the profile picture
    # Jake: possibly store the url of the image in the database, and have the url dynamically
    # added to pages

    # i dont know how to do it .JP
    userDP = db.Column(db.String(1024), db.ForeignKey('user.displayPicture'))
    dateTime = db.Column(db.DateTime(timezone=True), default=func.now())
    dataTitle = db.Column(db.String(200))
    data = db.Column(db.String(10000))
    # if possible create a field to store and display the number of views and the number of replies.


class Reply(db.Model):
    forumID = db.Column(db.Integer, db.ForeignKey('forumpost.forumid'))
    replyID = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(db.DateTime(timezone=True), default=func.now())
    data = data = db.Column(db.String(10000))
    email = db.Column(db.Integer, db.ForeignKey('user.email'))
    userFistName = db.Column(db.Integer, db.ForeignKey('user.firstName'))
    userLastName = db.Column(db.Integer, db.ForeignKey('user.lastName'))







