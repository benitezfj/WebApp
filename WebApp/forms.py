from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, FloatField, DateField, RadioField
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
    farmland = SelectField('Farmland', coerce=int)
    indices = SelectField('Index to Calculate', coerce=int, choices=[(1, 'NDVI'), (2, 'GNDVI'), (3, 'NDSI'), (4, 'RECL'), (5, 'NDWI'), (6, 'CWSI')])
    index_date = DateField('Index Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Find Location')
    def validate_dates(self, index_date):
        try:
            indexdate = datetime.date(index_date.data)
            print(indexdate)
        except ValueError:
            raise ValidationError("Invalid End Date or Start Date.")
        today_date = datetime.datetime.now()
        today_date = datetime.date(today_date.year, today_date.month, today_date.day)
        print(indexdate > today_date)
        if (indexdate > today_date):
            raise ValidationError("The Index Date can not be later the Current Date.")
            
    # cloud_cover =  FloatField("Cloud Coverage (%)", validators=[Optional()], default=60)    
    # start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    # coordinates = StringField('Coordinates', validators=[DataRequired()])
    # reducer = SelectField('Reducer', coerce=int, choices=[('1', 'Moderator'), ('2', 'Janitor')])
    # latitude = FloatField('Latitude', validators=[DataRequired()])           
    # longitude  = FloatField('Longitude', validators=[DataRequired()])    
    # def validate_cloud_cover(self, cloud_cover):
    #     try:
    #         cloud = float(cloud_cover.data)
    #     except ValueError:
    #         raise ValidationError("Invalid Expected Harvest Data.")
    #     if cloud != 60:
    #         raise ValidationError("Cloud Coverage must be a equal to 60%")
    #     if cloud > 100:
    #         raise ValidationError("Cloud Coverage cannot be greater than 100%")
    #     if cloud < 10:
    #         raise ValidationError("Cloud Coverage cannot be less than 10%")
    #     if cloud == "":
    #         raise ValidationError("Cloud Coverage cannot be empty.")



# ----------- New
# class IndexForm(FlaskForm):
#     latitude_1 = FloatField('Latitude 1', validators=[DataRequired()])
#     longitude_1  = FloatField('Longitude 1', validators=[DataRequired()])
#     latitude_2 = FloatField('Latitude 2', validators=[DataRequired()])
#     longitude_2  = FloatField('Longitude 2', validators=[DataRequired()])
#     submit = SubmitField('Find Index')
# -----------     
    
# ----------------------------Ingreso de Datos
# ----------------------------Cabecera
class InsertFarmlandForm(FlaskForm):
    name = StringField('Farmland Description', 
                              validators=[DataRequired(), Length(min=2, max=50)])
    croptype = SelectField('Crop Type', coerce=int)
    sowdate = DateField('Seedtime', format='%Y-%m-%d', validators=[DataRequired()])
    harvestdate = DateField('Harvest', format='%Y-%m-%d', validators=[DataRequired()])
    productexpected =  FloatField("Production Expected (tons)", validators=[Optional()], default=0)
    coordinates = StringField('Coordinates', validators=[DataRequired()])
    submit = SubmitField('Register the Crop Field.')
    
    def validate_production_expected(self, productexpected):
        try:
            prod_exp = float(productexpected.data)
        except ValueError:
            raise ValidationError("Invalid Production Harvest Data.")
        if prod_exp < 0:
            raise ValidationError("The Production Expected must be a Positive Value.")
        if prod_exp == "":
            raise ValidationError("The Production Expected can not be empty.")
            
    def validate_dates(self, sowdate, harvestdate):
        try:
            sow_date = datetime.date(sowdate.data)
            harvest_date = datetime.date(harvestdate.data)
        except ValueError:
            raise ValidationError("Invalid Seedtime or Harvest Time.")
        if sow_date >= harvest_date:
            raise ValidationError("The Harvest Date must be after the Seedtime.")
            
            
class HistoricalForm(FlaskForm):
    current_farm_id = SelectField('Current Farmland', coerce=int)
    historical_farm_id = SelectField('Historical Farmland', coerce=int)
    productobtained = FloatField("Production Obtained (tons)", validators=[Optional()], default=0)
    submit = SubmitField('Register the Historic Farmland.')
    
    def validate_production_obtained(self, productobtained):
        try:
            prod_obt = float(productobtained.data)
        except ValueError:
            raise ValidationError("Invalid Production Obtained Data.")
        if prod_obt < 0:
            raise ValidationError("The Production Obtained must be a Positive Value.")
        if prod_obt == "":
            raise ValidationError("The Production Obtained can not be empty.")


class FertilizarMapForm(FlaskForm):
    farmland = SelectField('Farmland', coerce=int)
    submit = SubmitField('Calculate Fertilizer Map')
    
            
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