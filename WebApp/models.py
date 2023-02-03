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
        return f"User('{self.username}', '{self.email}', '{self.role_id}')"


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)
    
    def __repr__(self):
        return f"Role('{self.description}')"


class Historical(db.Model):
    __tablename__ = 'historical'
    current_farm_id = db.Column(db.Integer, db.ForeignKey('farmlands.id'), primary_key=True)
    historical_farm_id = db.Column(db.Integer, db.ForeignKey('farmlands.id'), primary_key=True)
    product_obtained = db.Column(db.Float)
    def __repr__(self):
        return f"Historical('{self.current_farm_id}', '{self.historical_farm_id}')"


class Farmland(db.Model):
    __tablename__ = 'farmlands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    croptype_id = db.Column(db.Integer, db.ForeignKey('crops.id'))
    sow_date = db.Column(db.Date)
    harvest_date = db.Column(db.Date)
    product_expected = db.Column(db.Float)
    coordinates = db.Column(db.String(200), unique=True, nullable=False)
    current_farm = db.relationship('Historical', 
                                   foreign_keys=[Historical.current_farm_id], 
                                   backref=db.backref('current', lazy='joined'), 
                                   lazy=True)
    historical_farm = db.relationship('Historical', 
                                      foreign_keys=[Historical.historical_farm_id], 
                                      backref=db.backref('historical', lazy='joined'), 
                                      lazy=True)
    def __repr__(self):
        return f"Farmland('{self.name}', '{self.croptype_id}', '{self.sow_date}', '{self.harvest_date}', '{self.product_expected}', '{self.coordinates}')"


class Crop(db.Model):
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)
    farmlands = db.relationship('Farmland', backref='crop', lazy=True)
    
    def __repr__(self):
        return f"Crop('{self.description}')"
