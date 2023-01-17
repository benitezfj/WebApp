from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, FloatField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from WebApp.models import User, Role
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
            raise ValidationError('El nombre de usuario ya se ha utilizado.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('El email ya se ha utilizado.')
    
   
# Formulacion usado para registrar un usuario
class RegistrationRoleForm(FlaskForm):
    description = StringField('Role', 
                              validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Register')
    
    def validate_role(self, description):
        role_data = Role.query.filter_by(description=description.data).first()
        if role_data:
            raise ValidationError('El rol ya se encuentra creado.')
        
       
   
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

# ----------------------------Ingreso de Datos
# ----------------------------Cabecera
class InsertFarmlandForm(FlaskForm):
    croptype = SelectField('Tipo de Cultivo', coerce=int)
    sowdate = DateField('Fecha de Siembra', format='%Y-%m-%d', validators=[DataRequired()])
    harvestdate = DateField('Fecha de Cosecha', format='%Y-%m-%d', validators=[DataRequired()])
    productexpected =  FloatField("Producción Esperada", validators=[Optional()], default=0)
    submit = SubmitField('Registrar el Cultivo')
    
    def validate_production_expected(self, productexpected):
        try:
            prod_exp = float(productexpected.data)
        except ValueError:
            raise ValidationError("Produccion Esperada Invalida.")
        if prod_exp < 0:
            raise ValidationError("La producción esperada debe ser positiva")
        if prod_exp == "":
            raise ValidationError("La producción esperada no puede estar vacia.")
            
    def validate_dates(self, sowdate, harvestdate):
        try:
            sow_date = datetime.date(sowdate.data)
            harvest_date = datetime.date(harvestdate.data)
        except ValueError:
            raise ValidationError("La fecha de siembra o cosecha invalida.")
        if sow_date >= harvest_date:
            raise ValidationError("La fecha de cosecha debe ser posterior a la fecha de siembra.")
            
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