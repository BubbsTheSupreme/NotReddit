from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    username = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(200))
    bio = db.Column(db.String(120))
    posts = db.relationship('Post', backref='author')
    comments = db.relationship('Comment', backref='commenter')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), index=True)
    subs = db.Column(db.Integer)
    description = db.Column(db.String(120))
    posts = db.relationship('Post', backref='topic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    title = db.Column(db.String(30))
    content = db.Column(db.String(300))
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='thread')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pass

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))