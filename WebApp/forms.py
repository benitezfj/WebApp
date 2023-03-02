from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField, DateField, TextAreaField #, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from WebApp.models import User, Role, Crop, Farmland, SoilFarmland
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
    
   
class RegistrationRoleForm(FlaskForm):
    description = StringField('Role', 
                              validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Register')
    
    def validate_description(self, description):
        role_data = Role.query.filter_by(description=description.data).first()
        if role_data:
            raise ValidationError('That role is already created.')

            
class RegistrationCropForm(FlaskForm):
    description = StringField('Crop', 
                              validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Register')
    
    def validate_description(self, description):
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
    
    def validate_index_date(self, field):
        if (field.data > datetime.date.today()):
            raise ValidationError("The Index Date can not be later the Current Date.")
        # try:
        #     indexdate = datetime.date(index_date.data)
        #     print(indexdate)
        # except ValueError:
        #     raise ValidationError("Invalid End Date or Start Date.")
        # today_date = datetime.datetime.now()
        # today_date = datetime.date(today_date.year, today_date.month, today_date.day)
        # print(indexdate > today_date)
        # if (indexdate > today_date):
        #     raise ValidationError("The Index Date can not be later the Current Date.")
            

class InsertFarmlandForm(FlaskForm):
    name = StringField('Farmland Description', 
                              validators=[DataRequired(), Length(min=2, max=50)])
    croptype = SelectField('Crop Type', coerce=int)
    sowdate = DateField('Seedtime', format='%Y-%m-%d', validators=[DataRequired()])
    harvestdate = DateField('Harvest', format='%Y-%m-%d', validators=[DataRequired()])
    productexpected =  FloatField("Production Expected (Tons/ha)", validators=[Optional()], default=0)
    
    submit = SubmitField('Register the Crop Field.')
    
    def validate_name(self, field):
        if Farmland.query.filter_by(name=field.data).first():
            raise ValidationError('Farmland name already in use.')

    def validate_harvestdate(self, field):
        if field.data <= datetime.date.today():
            raise ValidationError("The Harvest Date must be a future date.")
        
    def validate_sowdate(self, field):
        if field.data >= self.harvestdate.data:
            raise ValidationError("Seed time must be before Harvest time.")
    
    def validate_productexpected(self, field):
        if field.data < 0:
            raise ValidationError("The Production Expected must be a Positive Value.")
            
            
class HistoricalForm(FlaskForm):
    current_farm = SelectField('Current Farmland', coerce=int)
    historical_farm = SelectField('Historical Farmland', coerce=int)
    productobtained = FloatField("Production Obtained (Tons/ha)", validators=[Optional()], default=0)
    submit = SubmitField('Register the Historic Farmland.')
    
    def validate_productobtained(self, field):
        if field.data < 0:
            raise ValidationError("The Production Obtained must be a Positive Value.")
        # if prod_obt == "":
        #     raise ValidationError("The Production Obtained can not be empty.")
        # try:
        #     prod_obt = float(productobtained.data)
        # except ValueError:
        #     raise ValidationError("Invalid Production Obtained Data.")


class FertilizarMapForm(FlaskForm):
    farmland = SelectField('Farmland', coerce=int)
    submit = SubmitField('Calculate Fertilizer Map')
        
    
class InsertHistoricalForm(FlaskForm):
    current_farm = SelectField('Current Farmland', coerce=int)
    # Historic
    croptype1 = SelectField('Crop Type', coerce=int, validators=[Optional()])
    sowdate1 = DateField('Historic Seed Date', format='%Y-%m-%d', validators=[Optional()])
    harvestdate1 = DateField('Historic Harvest Date', format='%Y-%m-%d', validators=[Optional()])
    productobtained = FloatField("Production Obtained (Tons/ha)", validators=[Optional()], default=0)
    
    # Type1
    nitrogen1 = FloatField("Nitrogen", validators=[Optional()], default=0)
    phosphorus1 = FloatField("Phosphorus", validators=[Optional()], default=0)
    potassium1 = FloatField("Potassium", validators=[Optional()], default=0)
    posology1 = FloatField("Posology N-P-K (Kg/ha)", validators=[Optional()], default=0)
    
    # Type2
    nitrogen2 = FloatField("Nitrogen", validators=[Optional()], default=0)
    phosphorus2 = FloatField("Phosphorus", validators=[Optional()], default=0)
    potassium2 = FloatField("Potassium", validators=[Optional()], default=0)
    posology2 = FloatField("Posology N-P-K (Kg/ha)", validators=[Optional()], default=0)
    
    # Type3
    nitrogen3 = FloatField("Nitrogen", validators=[Optional()], default=0)
    phosphorus3 = FloatField("Phosphorus", validators=[Optional()], default=0)
    potassium3 = FloatField("Potassium", validators=[Optional()], default=0)
    posology3 = FloatField("Posology N-P-K (Kg/ha)", validators=[Optional()], default=0)
    
    diseasesabnormalities = TextAreaField('Disease or Abnormality')
    diseasesabnormalitiesdate = DateField('Date of the Abnormality', format='%Y-%m-%d', validators=[Optional()])
    treatmentobservation = TextAreaField('Other relevant information (frost, drought)')
   
    submit = SubmitField('Register the Historic Farmland.')
        
    def validate_productobtained(self, field):
        if field.data < 0:
            raise ValidationError("The Production Obtained must be a Positive Value.")
        if field.data == "":
            raise ValidationError("The Production Obtained can not be empty.")
        # try:
        #     prod_obt = float(self.productobtained.data)
        # except ValueError:
        #     raise ValidationError("Invalid Production Obtained Data.")

    def validate_harvestdate1(self, field):
        if field.data >= datetime.date.today():
            raise ValidationError("The Harvest Date must be a past date.")
        # try:
        #     datetime.date(self.harvestdate1.data)
        # except ValueError:
        #     raise ValidationError("Invalid Seedtime or Harvest Time.")
            
    def validate_sowdate1(self, field):
        if field.data >= self.harvestdate1.data:
            raise ValidationError("The Seed Date must be before the Harvest Date.")
            
    def validate_diseasesabnormalitiesdate(self, field):
        if (self.sowdate1.data > field.data) and (field.data > self.harvestdate1.data):
            raise ValidationError("The Date of Diseases or Abnormalities must be between Seed Date and Harvest Date.")
        # try:
        #     sow_date = datetime.date(self.sowdate1.data)
        # except ValueError:
        #     raise ValidationError("Invalid Seedtime or Harvest Time.")



class SoilForm(FlaskForm):
    current_farm = SelectField('Current Farmland', coerce=int)
    name = StringField('Soil Test Name ', validators=[DataRequired(), Length(min=2, max=50)])
    soilsampledate = DateField('Soil Test Date', validators=[DataRequired()])
    depth = FloatField('Sampling Depth (cm)', validators=[DataRequired()], default=0)
    organicmatterlevel = FloatField('Organic Matter o N (%)', validators=[DataRequired()], default=0)
    phosphorus = FloatField('P', validators=[DataRequired()], default=0)
    phosphorus_unit = SelectField('P Unit', coerce=int)
    potassium = FloatField('K', validators=[DataRequired()], default=0)
    potassium_unit = SelectField('K Unit', coerce=int)
    calcium = FloatField('Ca', validators=[DataRequired()], default=0)
    calcium_unit = SelectField('Ca Unit', coerce=int)
    sand = FloatField('Sand', validators=[DataRequired()], default=0)
    slit = FloatField('Slit', validators=[DataRequired()], default=0)
    clay = FloatField('Clay', validators=[DataRequired()], default=0)
    sulfur = FloatField('Sulfur (mg/dm3)', validators=[DataRequired()], default=0)
    magnesium = FloatField('Mg (mg/dm3)', validators=[DataRequired()], default=0)
    boron = FloatField('B (mg/dm3)', validators=[DataRequired()], default=0)
    copper = FloatField('Cu (mg/dm3)', validators=[DataRequired()], default=0)
    zinc = FloatField('Zn (mg/dm3)', validators=[DataRequired()], default=0)
    manganese = FloatField('Mn (mg/dm3)', validators=[DataRequired()], default=0)
    
    submit = SubmitField('Register Soil Sample Data')
    
    # def validate_name(self, name):
    #     if SoilFarmland.query.filter_by(name=field.data).first():
    #         raise ValidationError('Soil Test name already in use.')
            
    def validate_depth(self, field):
        if (field.data < 0):
            raise ValidationError('Depth can not be a negative value.')

    def validate_organicmatterlevel(self, field):
        if (field.data < 0):
            raise ValidationError('Organic Matter Level can not be a negative value.')
        if (field.data > 100):
            raise ValidationError('Organic Matter Level can not higher than 100%.')

    def validate_phosphorus(self, field):
        if (field.data < 0):
            raise ValidationError('Phosphorus value can not be a negative value.')

    def validate_potassium(self, field):
        if (field.data < 0):
            raise ValidationError('Potassium value can not be a negative value.')

    def validate_calcium(self, field):
        if (field.data < 0):
            raise ValidationError('Calcium value can not be a negative value.')

    def validate_sand(self, field):
        if (field.data < 0):
            raise ValidationError('Sand value can not be a negative value.')

    def validate_slit(self, field):
        if (field.data < 0):
            raise ValidationError('Slit value can not be a negative value.')

    def validate_clay(self, field):
        if (field.data < 0):
            raise ValidationError('Clay value can not be a negative value.')

    def validate_sulfur(self, field):
        if (field.data < 0):
            raise ValidationError('Sulfur value can not be a negative value.')

    def validate_magnesium(self, field):
        if (field.data < 0):
            raise ValidationError('Magnesium value can not be a negative value.')

    def validate_boron(self, field):
        if (field.data < 0):
            raise ValidationError('Boron value can not be a negative value.')

    def validate_copper(self, field):
        if (field.data < 0):
            raise ValidationError('Copper value can not be a negative value.')

    def validate_zinc(self, field):
        if (field.data < 0):
            raise ValidationError('Zinc value can not be a negative value.')

    def validate_manganese(self, field):
        if (field.data < 0):
            raise ValidationError('Manganese value can not be a negative value.')
            
class CalculatorForm(FlaskForm):
    nitrogen = FloatField("N (kg/ha)", validators=[DataRequired()], default=0)
    phosphorus = FloatField("P (kg/ha)", validators=[DataRequired()], default=0)
    potassium = FloatField("K (kg/ha)", validators=[DataRequired()], default=0)
    submit = SubmitField('Calculate')
    
    def validate_nitrogen(self, field):
        if (field.data < 0):
            raise ValidationError('Nitrogen can not be a negative value.')
            
    def validate_phosphorus(self, field):
        if (field.data < 0):
            raise ValidationError('Phosphorus can not be a negative value.')
        
    def validate_potassium(self, field):
        if (field.data < 0):
            raise ValidationError('Potassium can not be a negative value.')

    
class InsertFullForm(FlaskForm):
    name = StringField('Farmland Description', validators=[DataRequired(), Length(min=2, max=50)])
    croptype = SelectField('Crop Type', coerce=int)
    sowdate = DateField('Seed Date', format='%Y-%m-%d', validators=[DataRequired()])
    harvestdate = DateField('Harvest Date', format='%Y-%m-%d', validators=[DataRequired()])
    productexpected =  FloatField("Production Expected (Tons/ha)", validators=[DataRequired()], default=0)
    
    # Historic
    croptype1 = SelectField('Crop Type', coerce=int)
    sowdate1 = DateField('Historic Seed Date', format='%Y-%m-%d', default=datetime.date.today)
    harvestdate1 = DateField('Historic Harvest Date', format='%Y-%m-%d', default=datetime.date.today)
    productobtained = FloatField("Production Obtained (Tons/ha)", default=0)
    # Type1
    nitrogen1 = FloatField("Nitrogen", default=0)
    phosphorus1 = FloatField("Phosphorus", default=0)
    potassium1 = FloatField("Potassium", default=0)
    posology1 = FloatField("Posology N-P-K (Kg/ha)", default=0)
    # Type2
    nitrogen2 = FloatField("Nitrogen", default=0)
    phosphorus2 = FloatField("Phosphorus", default=0)
    potassium2 = FloatField("Potassium", default=0)
    posology2 = FloatField("Posology N-P-K (Kg/ha)", default=0)
    # Type3
    nitrogen3 = FloatField("Nitrogen", default=0)
    phosphorus3 = FloatField("Phosphorus", default=0)
    potassium3 = FloatField("Potassium", default=0)
    posology3 = FloatField("Posology N-P-K (Kg/ha)", default=0)
    diseasesabnormalities = TextAreaField('Disease or Abnormality')
    diseasesabnormalitiesdate = DateField('Date of the Abnormality', format='%Y-%m-%d', default=datetime.date.today)
    treatmentobservation = TextAreaField('Other relevant information (frost, drought)')
    # Soil Test
    soilsampledate = DateField('Soil Test Date', default=datetime.date.today)
    depth = FloatField('Sampling Depth (cm)', default=0)
    organicmatterlevel = FloatField('Organic Matter o N (%)', default=0)
    phosphorus_1 = FloatField('P (ppm)', default=0)
    phosphorus_2 = FloatField('P (mg/dm3)', default=0)
    potassium_1 = FloatField('K (cmolc/dm3)', default=0)
    potassium_2 = FloatField('K (mg/dm3)', default=0)
    calcium_1 = FloatField('Ca (cmolc/dm3)', default=0)
    calcium_2 = FloatField('Ca (mg/dm3)', default=0)
    sand = FloatField('Sand', default=0)
    slit = FloatField('Slit', default=0)
    clay = FloatField('Clay', default=0)
    sulfur = FloatField('Sulfur (mg/dm3)', default=0)
    magnesium = FloatField('Mg (mg/dm3)', default=0)
    boron = FloatField('B (mg/dm3)', default=0)
    copper = FloatField('Cu (mg/dm3)', default=0)
    zinc = FloatField('Zn (mg/dm3)', default=0)
    manganese = FloatField('Mn (mg/dm3)', default=0)
   
    submit = SubmitField('Register the Crop Field.')    

    def validate_name(self, field):
        if Farmland.query.filter_by(name=field.data).first():
            raise ValidationError('Farmland name already in use.')

    def validate_harvestdate(self, field):
        if field.data <= datetime.date.today():
            raise ValidationError("The Harvest Date must be a future date.")
        
    def validate_sowdate(self, field):
        if field.data >= self.harvestdate.data:
            raise ValidationError("Seed time must be before Harvest time.")
    
    def validate_productexpected(self, field):
        if field.data < 0:
            raise ValidationError("The Production Expected must be a Positive Value.")
        # if self.productexpected.data == "":
        #     raise ValidationError("The Production Expected can not be empty.")
        

# ----------------------------Detalles
#class FertilizarForm(FlaskForm):
    # fertilizartype = SelectMultipleField('FertilizerType', coerce=int)
    # posology = StringField("Posology") #Agregar validadores
    # diseasesabnormalities = StringField('DiseaseOrAbnormality', validators=[Length(min=2, max=150)])
    # observation = StringField('Obs', validators=[Length(min=2, max=150)])
    # submit = SubmitField('Register Fertilizer Data')
    
# class TreatmentForm(FlaskForm):
    # treatment = StringField('Treatment')
    # treatmenttype = SelectMultipleField('TreatmentType', coerce=int)
    # treatmentdate = DateField('TreatmentDate')
    
    # treatmentobservation = StringField('Obs', validators=[Length(min=2, max=150)])
    # submit = SubmitField('Register Treatment Data')
    
# -----------------Test    