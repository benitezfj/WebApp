from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
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
