from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
        # posts serves as the relationship between the user and the user's posts. backref allows for access by calling the user, rather than the author from the Posts object.
    comments = db.relationship('Comment', backref='user', passive_deletes=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_title = db.Column(db.Text, nullable=False)
    ### page_count = db.Column(db.Integer, nullable=False)
    ### release_year = db.Column(db.Integer, nullable=False)
    ### book_author = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    ## author = db.Column(db.Integer)
        ## This technically can work to identify the author of the post, but the database must be able to verify the user's existence in the db.
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
        ## ondelete='CASCADE' will delete any posts that are associated with the specified user.
    comments = db.relationship('Comment', backref='post', passive_deletes=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    