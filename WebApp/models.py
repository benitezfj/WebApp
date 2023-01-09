from WebApp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# def position_query():
#     return Position.query

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    password = db.Column(db.String(60), nullable=False)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.position}')"


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref='position', lazy=True)
    
    def __repr__(self):
        return f"('{self.description}')"
    
