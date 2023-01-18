from WebApp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# def position_query():
#     return Position.query

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)
    
    def __repr__(self):
        return f"('{self.description}')"


class Farmland(db.Model):
    __tablename__ = 'farmlands'
    
    id = db.Column(db.Integer, primary_key=True)
    croptype_id = db.Column(db.Integer)
    sow_date = db.Column(db.Date)
    harvest_date = db.Column(db.Date)
    product_expected =  db.Column(db.Float)
    coordinates = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return f"Farmland('{self.croptype_id}', '{self.sow_date}', '{self.harvest_date}', '{self.product_expected}', '{self.coordinates}')"
    
    
class Crop(db.Model):
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)
    farmlands = db.relationship('Farmland', backref='crop', lazy=True)
    
    def __repr__(self):
        return f"('{self.description}')"