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



class HistoricFarmland(db.Model):
    __tablename__ = 'historicfarmlands'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    current_farm_id = db.Column(db.Integer, db.ForeignKey('farmlands.id'))
    croptype_id = db.Column(db.Integer, db.ForeignKey('crops.id'))
    sow_date = db.Column(db.Date)
    harvest_date = db.Column(db.Date)
    product_obtained = db.Column(db.Float)
    nitrogen_type1 = db.Column(db.Float)
    phosphorus_type1 = db.Column(db.Float)
    potassium_type1 = db.Column(db.Float)
    posology_type1 = db.Column(db.Float)
    nitrogen_type2 = db.Column(db.Float)
    phosphorus_type2 = db.Column(db.Float)
    potassium_type2 = db.Column(db.Float)
    posology_type2 = db.Column(db.Float)
    nitrogen_type3 = db.Column(db.Float)
    phosphorus_type3 = db.Column(db.Float)
    potassium_type3 = db.Column(db.Float)
    posology_type3 = db.Column(db.Float)
    diseases_abnormalities = db.Column(db.String(150))
    diseases_abnormalitiesdate = db.Column(db.Date)
    observation = db.Column(db.String(150))

    def __repr__(self):
        return f"HistoricFarmland('{self.current_farm_id}', '{self.croptype_id}', '{self.sow_date}', '{self.harvest_date}', '{self.product_obtained}', '{self.nitrogen_type1}', '{self.phosphorus_type1}', '{self.potassium_type1}', '{self.posology_type1}', '{self.nitrogen_type2}', '{self.phosphorus_type2}', '{self.potassium_type2}', '{self.posology_type2}', '{self.nitrogen_type3}', '{self.phosphorus_type3}', '{self.potassium_type3}', '{self.posology_type3}', '{self.diseases_abnormalities}', '{self.diseases_abnormalitiesdate}', '{self.observation}')"



class SoilFarmland(db.Model):
    __tablename__ = 'soilfarmlands'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    current_farm_id = db.Column(db.Integer, db.ForeignKey('farmlands.id'))
    # name = db.Column(db.String(50), unique=True, nullable=False)
    soil_date = db.Column(db.Date)
    soil_depth = db.Column(db.Float)
    soil_organic_level = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    calcium = db.Column(db.Float)
    phosphorus_unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    potassium_unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    calcium_unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    sand = db.Column(db.Float)
    slit = db.Column(db.Float)
    clay = db.Column(db.Float)
    sulfur = db.Column(db.Float)
    magnesium = db.Column(db.Float)
    boron = db.Column(db.Float)
    copper = db.Column(db.Float)
    zinc = db.Column(db.Float)
    manganese = db.Column(db.Float)
    
    def __repr__(self):
        return f"SoilFarmland('{self.current_farm_id}', '{self.soil_date}', '{self.soil_depth}', '{self.soil_organic_level}', '{self.phosphorus_ppm}', '{self.phosphorus_mg}', '{self.potassium_cmolc}', '{self.potassium_mg}', '{self.calcium_cmolc}', '{self.calcium_mg}', '{self.sand}', '{self.slit}', '{self.clay}', '{self.sulfur}', '{self.magnesium}', '{self.boron}', '{self.copper}', '{self.zinc}', '{self.manganese}')"

class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)
    soilfarmland_phosphorus = db.relationship('SoilFarmland', foreign_keys=[SoilFarmland.phosphorus_unit_id], backref=db.backref('phosphorus_unit', lazy='joined'), lazy=True)
    soilfarmland_potassium = db.relationship('SoilFarmland', foreign_keys=[SoilFarmland.potassium_unit_id],  backref=db.backref('potassium_unit', lazy='joined'), lazy=True)
    soilfarmland_calcium = db.relationship('SoilFarmland', foreign_keys=[SoilFarmland.calcium_unit_id],    backref=db.backref('calcium_unit', lazy='joined'), lazy=True)
    
    
    def __repr__(self):
        return f"Unit('{self.description}')"
    
    
class Farmland(db.Model):
    __tablename__ = 'farmlands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    croptype_id = db.Column(db.Integer, db.ForeignKey('crops.id'))
    sow_date = db.Column(db.Date)
    harvest_date = db.Column(db.Date)
    product_expected = db.Column(db.Float)
    coordinates = db.Column(db.String(200), unique=True, nullable=False)
    historicalfarmlands = db.relationship('HistoricFarmland', backref='farmland', lazy=True)
    soilfarmlands = db.relationship('SoilFarmland', backref='farmland', lazy=True)
    # current_farm = db.relationship('Historical', 
    #                                foreign_keys=[Historical.current_farm_id], 
    #                                backref=db.backref('current', lazy='joined'), 
    #                                lazy=True)
    # historical_farm = db.relationship('Historical', 
    #                                   foreign_keys=[Historical.historical_farm_id], 
    #                                   backref=db.backref('historical', lazy='joined'), 
    #                                   lazy=True)
    
    
    def __repr__(self):
        return f"Farmland('{self.name}', '{self.croptype_id}', '{self.sow_date}', '{self.harvest_date}', '{self.product_expected}', '{self.coordinates}')"


class Crop(db.Model):
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True, nullable=False)
    farmlands = db.relationship('Farmland', backref='crop', lazy=True)
    
    def __repr__(self):
        return f"Crop('{self.description}')"


# class Historical(db.Model):
#     __tablename__ = 'historical'
#     current_farm_id = db.Column(db.Integer, db.ForeignKey('farmlands.id'), primary_key=True)
#     historical_farm_id = db.Column(db.Integer, db.ForeignKey('farmlands.id'), primary_key=True)
#     product_obtained = db.Column(db.Float)
#     def __repr__(self):
#         return f"Historical('{self.current_farm_id}', '{self.historical_farm_id}')"
    
    
# class HistoricFarmland(db.Model):
#     __tablename__ = 'historicfarmlands'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     current_farm_id = db.Column(db.Integer, db.ForeignKey('farmlands.id'))
#     name = db.Column(db.String(50), unique=True, nullable=False)
#     croptype_id = db.Column(db.Integer, db.ForeignKey('crops.id'))
#     sow_date = db.Column(db.Date)
#     harvest_date = db.Column(db.Date)
#     product_obtained = db.Column(db.Float)
#     product_expected = db.Column(db.Float)
#     coordinates = db.Column(db.String(200), unique=True, nullable=False)
    
#     def __repr__(self):
#         return f"HistoricFarmland('{self.current_farm_id}', '{self.name}', '{self.croptype_id}', '{self.sow_date}', '{self.harvest_date}', '{self.product_obtained}', '{self.product_expected}', '{self.coordinates}')"