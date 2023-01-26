from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, FloatField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from WebApp.models import User, Role, Crop
import datetime
'''
wtforms
    StringField: Crea campo en el que se permite cargar cadena de textos
    PasswordField: Crea campo en el que se permite cargar cadena contraseñas 
    SubmitField:
    BooleanField:
    wtforms.validators: Validaciones de los datos cargados.
        DataRequired: El dato debe de ser cargado.
        Length: Longitud exacta en base a un maximo y minimo.
        Email: el tipo de string debe seguir el formato de un email.
        EqualTo: el valor cargado en el cambio debe ser igual a alguna condicion.
        
    
'''
# crop = [(1, 'Soja'), (2, 'Maíz'), (3, 'Trigo'), (4, 'Oliva'), (5, 'Arroz'), (6, 'Fruta'), (7, 'Raíces y Tubérculos'), (8, 'Vegetales'), (9, 'Azúcar')]
       

# ('Position', query_factory=position_query, allow_blank=False, get_pk=lambda a: a.id)
# Formulacion usado para registrar un usuario
class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                       validators=[DataRequired(), Email()])
    role = SelectField('User Role', coerce=int)
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    
   
# Formulacion usado para registrar un usuario
class RegistrationRoleForm(FlaskForm):
    description = StringField('Role', 
                              validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Register')
    
    def validate_role(self, description):
        role_data = Role.query.filter_by(description=description.data).first()
        if role_data:
            raise ValidationError('That role is already created.')
            
class RegistrationCropForm(FlaskForm):
    description = StringField('Crop', 
                              validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Register')
    
    def validate_crop(self, description):
        crop_data = Crop.query.filter_by(description=description.data).first()
        if crop_data:
            raise ValidationError('That crop is already created.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class MapForm(FlaskForm):
    latitude = FloatField('Latitude', validators=[DataRequired()])           
    longitude  = FloatField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Find Location')

# ----------- New
class IndexForm(FlaskForm):
    indices = SelectField('Indices', coerce=int)
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    reducer = SelectField('Reducer', coerce=int)
    latitude_1 = FloatField('Latitude 1', validators=[DataRequired()])
    longitude_1  = FloatField('Longitude 1', validators=[DataRequired()])
    latitude_2 = FloatField('Latitude 2', validators=[DataRequired()])
    longitude_2  = FloatField('Longitude 2', validators=[DataRequired()])
    cloud_cover =  FloatField("Cloud Cover (%)", validators=[Optional()], default=0)
    submit = SubmitField('Find Index')
# -----------     
    
# ----------------------------Ingreso de Datos
# ----------------------------Cabecera
class InsertFarmlandForm(FlaskForm):
    croptype = SelectField('Crop Type', coerce=int)
    sowdate = DateField('Seedtime', format='%Y-%m-%d', validators=[DataRequired()])
    harvestdate = DateField('Harvest', format='%Y-%m-%d', validators=[DataRequired()])
    productexpected =  FloatField("Expected Harvest (tons)", validators=[Optional()], default=0)
    submit = SubmitField('Register the Crop Field.')
    coordinates = StringField('Coordinates')
    
    def validate_production_expected(self, productexpected):
        try:
            prod_exp = float(productexpected.data)
        except ValueError:
            raise ValidationError("Invalid Expected Harvest Data.")
        if prod_exp < 0:
            raise ValidationError("The Expected Harvest must be a Positive Value.")
        if prod_exp == "":
            raise ValidationError("The Expected Harvest can not be empty.")
            
    def validate_dates(self, sowdate, harvestdate):
        try:
            sow_date = datetime.date(sowdate.data)
            harvest_date = datetime.date(harvestdate.data)
        except ValueError:
            raise ValidationError("Invalid Seedtime or Harvest Time.")
        if sow_date >= harvest_date:
            raise ValidationError("The Harvest Date must be after the Seedtime.")
            
# ----------------------------Detalles
class FertilizarForm(FlaskForm):
    fertilizartype = SelectMultipleField('FertilizerType', coerce=int)
    posology = StringField("Posology") #Agregar validadores
    diseasesabnormalities = StringField('DiseaseOrAbnormality', validators=[Length(min=2, max=150)])
    observation = StringField('Obs', validators=[Length(min=2, max=150)])
    submit = SubmitField('Register Fertilizer Data')
    
class TreatmentForm(FlaskForm): 
    treatment = StringField('Treatment')
    treatmenttype = SelectMultipleField('TreatmentType', coerce=int)
    treatmentdate = DateField('TreatmentDate')
    posology = StringField("Posology")
    treatmentobservation = StringField('Obs', validators=[Length(min=2, max=150)])
    submit = SubmitField('Register Treatment Data')
    
class SoilForm(FlaskForm):    
    soilsampledate = DateField('TreatmentDate')
    location = FloatField('Location')
    depth = FloatField('Depth')
    nitrogenlevel = FloatField('NitrogenLevel')
    organicmatterlevel = FloatField('OrganicMatterLevel')
    phosphoruslevel = FloatField('PhosphorusLevel')
    potassiumlevel = FloatField('PotassiumLevel')
    soilmoisture = FloatField('SoilMoisture')
    submit = SubmitField('Register Soil Sample Data')