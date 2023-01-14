from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, FloatField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from WebApp.models import User, Position
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
    position = SelectField('Position', coerce=int)
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
class RegistrationPositionForm(FlaskForm):
    description = StringField('Position', 
                              validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Register')
    
    def validate_position(self, description):
        position_data = Position.query.filter_by(description=description.data).first()
        if position_data:
            raise ValidationError('La posición ya se encuentra creada.')
        
       
   
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
class InsertCropForm(FlaskForm):
    croptype = SelectMultipleField('Crop Type', coerce=int)
    sowdate = DateField('SowDate ', format='%d/%m/%Y', validators=[DataRequired()])
    harvesdate = DateField('HarvesDate', format='%d/%m/%Y', validators=[DataRequired()])
    productexpected =  StringField("ProductionExpected", [Optional()], default=0)
    submit = SubmitField('Register the crop')
    
    def validate_production_expected(self, productexpected):
        try:
            price = float(productexpected.data)
        except ValueError:
            raise ValidationError("Produccion Esperada Invalida.")
        if price < 0:
            raise ValidationError("La producción esperada debe ser positiva")
        if price == "":
            raise ValidationError("La producción esperada no puede estar vacia.")

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