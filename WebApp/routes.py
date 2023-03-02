from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from WebApp import db, bcrypt
from WebApp.forms import RegistrationForm, LoginForm, RegistrationRoleForm, MapForm, RegistrationCropForm, FertilizarMapForm, InsertHistoricalForm, SoilForm, InsertFarmlandForm, CalculatorForm #, HistoricalForm, InsertFullForm 
from WebApp.models import User, Role, Farmland, Crop, HistoricFarmland, SoilFarmland, Unit
from fertilizer.calculator_spinach import spinachFertilizer
from fertilizer.fertilizerCalculator import fertilizerCalculator
from earthengine.methods import get_image_collection_asset, get_fertilizer_map
# from sqlalchemy.orm import aliased
import numpy as np
import datetime as dt
import ee

# earthengine authenticate
ee.Initialize()
# from WebApp.config import Config
# EE_CREDENTIALS = ee.ServiceAccountCredentials(config.EE_ACCOUNT, config.EE_PRIVATE_KEY_FILE)
# ee.Initialize(EE_CREDENTIALS)

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    return render_template('home.html')


@main.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    pos = [(p.id, p.description) for p in Role.query.order_by(Role.description).all()]
    form.role.choices = pos
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, 
                    email = form.email.data, 
                    role_id = form.role.data, 
                    password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main.route("/newrole", methods=['GET','POST'])
@login_required
def registerrole():
    form = RegistrationRoleForm()
    if form.validate_on_submit():
        pos = Role(description = form.description.data)
        db.session.add(pos)
        db.session.commit()
        flash('A new role has been registered', 'success')
        return redirect(url_for('main.login'))
    return render_template('position.html', title='Role', form=form)


@main.route("/newcrop", methods=['GET','POST'])
@login_required
def registercrop():
    form = RegistrationCropForm()
    if form.validate_on_submit():
        pos = Crop(description = form.description.data)
        db.session.add(pos)
        db.session.commit()
        flash('A new crop type has been registered.', 'success')
        return redirect(url_for('main.login'))
    return render_template('croptype.html', title='Crop', form=form)


@main.route("/login", methods=['GET','POST'])
def login():
    # Redireccionaar a /list
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@main.route("/farmlandlist")
@login_required
def land_selection():
    lands = db.session.query(Farmland).join(Crop).add_columns(Farmland.id, Farmland.name, Crop.description, Farmland.sow_date, Farmland.harvest_date, Farmland.product_expected, Farmland.coordinates).filter(Farmland.croptype_id == Crop.id)
    return render_template('land_selection.html', title='Farmland List', lands=lands)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/vegetationindex", methods=['GET','POST'])
@login_required
def maps():
    form = MapForm()
    form.farmland.choices = [(f.id, f.name) for f in Farmland.query.order_by(Farmland.name).all()]
    
    if form.validate_on_submit(): 
        farm_id     = form.farmland.data
        index       = form.indices.data
        index_date  = form.index_date.data
        coverage    = 60

        index_date  = index_date.strftime("%Y-%m-%d")
        
        lands           = Farmland.query.get_or_404(farm_id)
        farmland_name   = lands.name
        coord           = np.array(lands.coordinates.split(','))
        
        roi             = ee.Geometry.Polygon([float(i) for i in coord])
        lon             = ee.Number(roi.centroid().coordinates().get(0)).getInfo();
        lat             = ee.Number(roi.centroid().coordinates().get(1)).getInfo();
        
        map_url, index_name, end_date = get_image_collection_asset(platform='sentinel', 
                                                                 sensor='2', 
                                                                 product='BOA', 
                                                                 cloudy = coverage, 
                                                                 date_to = index_date, 
                                                                 roi = roi, 
                                                                 index = index)
        
        map_json = {'map_url': map_url, 
                    'latitude': lat, 
                    'longitude': lon,
                    'farmland_name': farmland_name,
                    'index_name': index_name,
                    'indexdate': end_date,
                    'cover': coverage}    
        
        return render_template('results.html', title='Vegetation Index', maps=map_json, form=form)
    return render_template('input.html', title='Vegetation Index', form=form) 


@main.route("/fertilizermap", methods=['GET','POST'])
@login_required
def fertilizer_maps():
    form = FertilizarMapForm()
    form.farmland.choices = [(f.id, f.name) for f in Farmland.query.order_by(Farmland.name).all()]
    
    if form.validate_on_submit(): 
        farm_id         = form.farmland.data
        
        coverage        = 60
        lands           = Farmland.query.get_or_404(farm_id)
        farmland_name   = lands.name
        coord           = np.array(lands.coordinates.split(','))
        production_exp  = lands.product_expected
        
        roi             = ee.Geometry.Polygon([float(i) for i in coord])
        lon             = ee.Number(roi.centroid().coordinates().get(0)).getInfo();
        lat             = ee.Number(roi.centroid().coordinates().get(1)).getInfo();

        nutrients = spinachFertilizer(production_exp)
        nitrogen, potassium, phosphorus = nutrients[0:3]
        
        fertilizer_measure, diff_blend = fertilizerCalculator(n=nitrogen, p=potassium, k=phosphorus, db=2)

        fertilizer_measure = np.array(fertilizer_measure)
        diff_blend = np.array(diff_blend)[0]
        
        # Extract amount of fertilizer kg/ha
        amount_fertilizer = []
        for index, value in np.ndenumerate(fertilizer_measure):
                    if index[1] == 0:
                        amount_fertilizer.append(value)
        
        b = [0.7, 1, 1.1]
        amount_fertilizer = np.outer(np.array(b), np.array(amount_fertilizer))

        # NPK Commercial
        type_fertilizer = np.delete(fertilizer_measure, 0, axis=1).astype(int)
        
        fertilizer = []
        fertilizer.append(production_exp)
        fertilizer.append(amount_fertilizer)
        fertilizer.append(type_fertilizer)
        fertilizer.append(diff_blend)
        print(fertilizer)
        
        
        map_url, end_date = get_fertilizer_map(platform='sentinel', 
                                     sensor='2', 
                                     product='BOA', 
                                     cloudy = coverage, 
                                     roi = roi, 
                                     reducer = 'first')
        print(map_url)

        map_json = {'map_url': map_url, 
                    'latitude': lat, 
                    'longitude': lon,
                    'farmland_name': farmland_name,
                    'posologydate': end_date,
                    'production_exp': production_exp}
        
        print(map_json)
        return render_template('results_fertilizer.html', title='Maps', maps=map_json, form=form, nutrient=nutrients, fertilizer_measure = fertilizer)
    return render_template('input_fertilizer.html', title='Maps', form=form)


@main.route("/calculator", methods=['GET','POST'])
@login_required
def calculator():
    form = CalculatorForm()
    
    if form.validate_on_submit(): 
        nitro = form.nitrogen.data
        phosp = form.phosphorus.data
        pota = form.potassium.data
        
        fertilizer_measure, diff_blend = fertilizerCalculator(n=nitro, p=phosp, k=pota, db=2)

        fertilizer_measure = np.array(fertilizer_measure)
        diff_blend = np.array(diff_blend)[0]
                
        # Extract amount of fertilizer kg/ha
        amount_fertilizer = []
        for index, value in np.ndenumerate(fertilizer_measure):
                    if index[1] == 0:
                        amount_fertilizer.append(value)
        
        b = [0.7, 1, 1.1]
        amount_fertilizer = np.outer(np.array(b), np.array(amount_fertilizer))

        # NPK Commercial
        type_fertilizer = np.delete(fertilizer_measure, 0, axis=1).astype(int)
        
        print(fertilizer_measure,", ",diff_blend, ", ", amount_fertilizer, ", ", type_fertilizer)
        return render_template('results_calculator.html', title='Sanzar Calculator', form = form, fertilizer_measure = fertilizer_measure)
    return render_template('input_calculator.html', title='Sanzar Calculator', form=form) 


@main.route("/inserthistoric", methods=['GET','POST'])
@login_required
def insert_historical_data():
    form = InsertHistoricalForm()
    form.current_farm.choices = [(f.id, f.name) for f in Farmland.query.order_by(Farmland.name).filter(Farmland.harvest_date > dt.date(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)).all()]
    form.croptype1.choices = [(c.id, c.description) for c in Crop.query.order_by(Crop.description).all()]
    print(form.validate_on_submit())
    if form.validate_on_submit():
        # current_farm    = Farmland.query.get_or_404(form.current_farm.data)
        
        print(form.current_farm.data, 
              form.croptype1.data, 
              form.sowdate1.data, 
              form.harvestdate1.data,
              form.productobtained.data, 
              form.nitrogen1.data,
              form.phosphorus1.data,
              form.potassium1.data,
              form.posology1.data,
              form.nitrogen2.data,
              form.phosphorus2.data,
              form.potassium2.data,
              form.posology2.data,
              form.nitrogen3.data,
              form.phosphorus3.data,
              form.potassium3.data,
              form.posology3.data,
              form.diseasesabnormalities.data,
              form.diseasesabnormalitiesdate.data,
              form.treatmentobservation.data)

        hist = HistoricFarmland(current_farm_id = form.current_farm.data,
                        		croptype_id = form.croptype1.data,
                        		sow_date = form.sowdate1.data,
                        		harvest_date = form.harvestdate1.data,
                        		product_obtained = form.productobtained.data,
                        		nitrogen_type1 = form.nitrogen1.data,
                        		phosphorus_type1 = form.phosphorus1.data,
                        		potassium_type1 = form.potassium1.data,
                        		posology_type1 = form.posology1.data,
                        		nitrogen_type2 = form.nitrogen2.data,
                        		phosphorus_type2 = form.phosphorus2.data,
                        		potassium_type2 = form.potassium2.data,
                        		posology_type2 = form.posology2.data,
                        		nitrogen_type3 = form.nitrogen3.data,
                        		phosphorus_type3 = form.phosphorus3.data,
                        		potassium_type3 = form.potassium3.data,
                        		posology_type3 = form.posology3.data,
                        		diseases_abnormalities = form.diseasesabnormalities.data,
                        		diseases_abnormalitiesdate = form.diseasesabnormalitiesdate.data,
                        		observation = form.treatmentobservation.data)
        
        db.session.add(hist)
        db.session.commit()
        flash('A historical farmland was assigned to a current one.', 'success')
        return redirect(url_for('main.login'))
    return render_template('historical_2.html', title='Historical', form=form)

        # CurrentCrop = aliased(Crop)
        # HistoricalCrop = aliased(Crop)
        # historic_table = db.session.query(HistoricFarmland) \
        # 	.join(Farmland, HistoricFarmland.current_farm_id == Farmland.id) \
        # 	.join(CurrentCrop, HistoricFarmland.croptype_id == CurrentCrop.id) \
        # 	.join(HistoricalCrop, HistoricFarmland.croptype_id == HistoricalCrop.id) \
        # 	.add_columns(HistoricFarmland.name.label('historic_name'), 
        # 		HistoricalCrop.description.label('last_crop'),
        # 		HistoricFarmland.sow_date.label('current_seed_time'), 
        # 		HistoricFarmland.harvest_date.label('last_harvest_date'), 
        # 		HistoricFarmland.product_obtained.label('product_obtained'),
        # 		Farmland.name.label('current_name'), 
        # 		CurrentCrop.description.label('current_crop'), 
        # 		Farmland.sow_date.label('current_seed_time'), 
        # 		Farmland.harvest_date.label('next_harvest_date'), 
        # 		Farmland.product_expected.label('current_production'), 
        # 		Farmland.coordinates.label('coordinates')) #.all()
        # 'Soja 2.2', 'Soja', datetime.date(2023, 2, 1), datetime.date(2022, 12, 31),   100.0, 'Soja 2', 'Soja', datetime.date(2023, 2, 1), datetime.date(2023, 3, 31), 100.0, '-55.04562,-25.45641,-55.044751,-25.456226,-55.044478,-25.457073,-55.045358,-25.457296,-55.04562,-25.45641'
        # hist = HistoricFarmland(current_farm_id  = form.current_farm.data,
        #                         name             = form.name.data,
        #                         product_obtained = form.productobtained.data,
        #                         croptype_id      = form.croptype.data,
        #                         sow_date         = form.sowdate.data,
        #                         harvest_date     = form.harvestdate.data,
        #                         product_expected = current_farm.product_expected,
        #                         coordinates      = current_farm.coordinates)


@main.route("/soiltest", methods=['GET','POST'])
@login_required
def insert_soiltest():
    form = SoilForm()
    # https://stackoverflow.com/questions/27451693/display-two-fields-side-by-side-in-a-bootstrap-form
    form.current_farm.choices = [(f.id, f.name) for f in Farmland.query.order_by(Farmland.name).filter(Farmland.harvest_date > dt.date(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)).all()]
    form.phosphorus_unit.choices = [(c.id, c.description) for c in Unit.query.order_by(Unit.description).all()]
    form.potassium_unit.choices = [(c.id, c.description) for c in Unit.query.order_by(Unit.description).all()]
    form.calcium_unit.choices = [(c.id, c.description) for c in Unit.query.order_by(Unit.description).all()]
    if form.validate_on_submit():
        # current_farm    = Farmland.query.get_or_404(form.current_farm.data)
        
        print(form.current_farm.data,
              form.name.data, 
              form.soilsampledate.data, 
              form.depth.data,
              form.organicmatterlevel.data, 
              form.phosphorus.data,
              form.phosphorus_unit.data,
              form.potassium.data,
              form.potassium_unit.data,
              form.calcium.data,
              form.calcium_unit.data,
              form.sand.data,
              form.slit.data,
              form.clay.data,
              form.sulfur.data,
              form.magnesium.data,
              form.boron.data,
              form.copper.data,
              form.zinc.data,
              form.manganese.data)

        # soil = SoilFarmland(current_farm_id = form.current_farm.data,
        #                     soil_date = form.soilsampledate.data,
        #                     soil_depth = form.depth.data,
        #                     soil_organic_level = form.organicmatterlevel.data,
        #                     phosphorus = form.phosphorus.data,
        #                     phosphorus_unit_id = form.phosphorus_unit.data,
        #                     potassium = form.potassium.data,
        #                     potassium_unit_id = form.potassium_unit.data,
        #                     calcium = form.calcium.data,
        #                     calcium_unit_id = form.calcium_unit.data,
        #                     sand = form.sand.data,
        #                     slit = form.slit.data,
        #                     clay = form.clay.data,
        #                     sulfur = form.sulfur.data,
        #                     magnesium = form.magnesium.data,
        #                     boron = form.boron.data,
        #                     copper = form.copper.data,
        #                     zinc = form.zinc.data,
        #                     manganese = form.manganese.data)

        # db.session.add(soil)
        # db.session.commit()
        # flash('A New Soil Test was assigned to a current farmland.', 'success')
        # return redirect(url_for('main.login'))
    return render_template('soiltest.html', title='Soil Test', form=form)



@main.route("/newfarmland", methods=['GET', 'POST'])
@login_required
def insert_farmland_data():
    form = InsertFarmlandForm()
    crops = [(c.id, c.description) for c in Crop.query.order_by(Crop.description).all()]
    form.croptype.choices = crops
    # print(form.validate_on_submit())
    # print(request.get_json())
    # print((form.form_errors))
    # print(form.errors)
    # if form.is_submitted():
    #     print("submitted")
    # if form.validate():
    #     print("valid")
    # print(form.errors)
    # print(form.name.errors)
    if form.validate_on_submit(): 
        request_data = request.get_json()
        print("Test")
        descrip = request_data.get('name')
        crop = int(request_data.get('croptype'))
        coord = request_data.get('coordinates').replace("[","").replace("]","").replace("\n","").replace(" ","")
        sow = dt.datetime.strptime(request_data.get('sowdate'), '%Y-%m-%d').date()
        harvest = dt.datetime.strptime(request_data.get('harvestdate'), '%Y-%m-%d').date()
        product_expected = float(request_data.get('productexpected'))
        
        print(request.method)
        
        print(descrip, 
    	      crop, 
              coord,
    	      sow, 
    	      harvest, 
    	      product_expected)
        crop = Farmland(name = descrip,
                        croptype_id = crop,
                        sow_date = sow,
                        harvest_date = harvest,
                        product_expected = product_expected,
                        coordinates = coord)
        db.session.add(crop)
        db.session.commit()

        flash('A New Crop Field has been Registered', 'success')
        return redirect(url_for('main.login'))
    return render_template('crop3.html', title='Insert a New Crop Field', form=form)

# @main.route("/farmland", methods=['GET', 'POST'])
# @login_required
# def insert_farmland_data():
#     form = InsertFarmlandForm()
#     crops = [(c.id, c.description) for c in Crop.query.order_by(Crop.description).all()]
#     form.croptype.choices = crops
#     print(request.method)
#     if form.validate_on_submit(): 
#         request_data = request.get_json()
#         # descrip = request_data['name']
#         descrip = request_data.get('name')
#         # coord = request_data['coordinates'].replace("[","").replace("]","").replace("\n","").replace(" ","")
#         coord = request_data.get('coordinates').replace("[","").replace("]","").replace("\n","").replace(" ","")

#         # crop = int(request_data['croptype'])
#         crop = int(request_data.get('croptype'))
#         # sow = dt.datetime.strptime(request_data['sowdate'], '%Y-%m-%d').date()
#         sow = dt.datetime.strptime(request_data.get('sowdate'), '%Y-%m-%d').date()
#         # harvest = dt.datetime.strptime(request_data['harvestdate'], '%Y-%m-%d').date()
#         harvest = dt.datetime.strptime(request_data.get('harvestdate'), '%Y-%m-%d').date()
#         # product = float(request_data['productexpected'])
#         product = float(request_data.get('productexpected'))
        
#         print(request.method,descrip,crop,sow,harvest,coord,product)
#         # print(request.method, "Test")
#         crop = Farmland(name = descrip,
#                         croptype_id = crop,
#                         sow_date = sow,
#                         harvest_date = harvest,
#                         coordinates = coord,
#                         product_expected = product)
        
#         db.session.add(crop)
#         db.session.commit()
#         flash('A New Crop Field has been Registered', 'success')
#         return redirect(url_for('main.home'))
        
#         # return redirect(url_for('main.home'))
#     return render_template('crop.html', title='Insert a New Crop Field', form=form)


# print(form.validate_production_expected())
# Debug valitador https://stackoverflow.com/questions/13585663/flask-wtfform-flash-does-not-display-errors/13587339#13587339
# https://stackoverflow.com/questions/62134860/wtforms-validate-on-submit-with-empty-values-behaviour
# Verficar valores devueltos por js in crop2
# https://stackoverflow.com/questions/38664088/flask-404-for-post-request
# Test
# @main.route("/newfarmland", methods=['GET', 'POST'])
# @login_required
# def insert_farmland_data():
#     form = InsertFullForm()
#     crops = [(c.id, c.description) for c in Crop.query.order_by(Crop.description).all()]
#     form.croptype.choices = crops
#     form.croptype1.choices = crops

#     # print(form.validate_on_submit())
#     # print(request.get_json())
#     # print((form.form_errors))
#     # print(form.errors)
#     # if form.is_submitted():
#     #     print("submitted")
#     # if form.validate():
#     #     print("valid")
#     # print(form.errors)
#     # print(form.name.errors)
#     if form.validate_on_submit(): 
#         request_data = request.get_json()
#         print("Test")
#         descrip = request_data.get('name')
#         crop = int(request_data.get('croptype'))
#         coord = request_data.get('coordinates').replace("[","").replace("]","").replace("\n","").replace(" ","")
#         sow = dt.datetime.strptime(request_data.get('sowdate'), '%Y-%m-%d').date()
#         harvest = dt.datetime.strptime(request_data.get('harvestdate'), '%Y-%m-%d').date()
#         product_expected = float(request_data.get('productexpected'))
        
        
#         print(request.method)
        
#         historic_flag = request_data.get('historic')
#         soil_flag = request_data.get('soil')
        
#         print(historic_flag,soil_flag)
        
#         print(descrip,crop,sow,harvest,coord,product_expected)
#         crop = Farmland(name = descrip,
#                         croptype_id = crop,
#                         sow_date = sow,
#                         harvest_date = harvest,
#                         product_expected = product_expected,
#                         coordinates = coord)
#         db.session.add(crop)
#         db.session.commit()
#         # crop.id
        
#         if(historic_flag=="Yes"):
#             # farm_id = crop.id
#             croptype1 = int(request_data.get('croptype'))
#             sowdate1 = dt.datetime.strptime(request_data.get('sowdate1'), '%Y-%m-%d').date()
#             harvestdate1 = dt.datetime.strptime(request_data.get('harvestdate1'), '%Y-%m-%d').date()
#             product_obtained = float(request_data.get('productobtained'))
#             nitrogen1 = float(request_data.get('nitrogen1'))
#             phosphorus1 = float(request_data.get('phosphorus1'))
#             potassium1 = float(request_data.get('potassium1'))
#             posology1 = float(request_data.get('posology1'))
#             nitrogen2 = float(request_data.get('nitrogen2'))
#             phosphorus2 = float(request_data.get('phosphorus2'))
#             potassium2 = float(request_data.get('potassium2'))
#             posology2 = float(request_data.get('productobtained'))
#             nitrogen3 = float(request_data.get('posology2'))
#             phosphorus3 = float(request_data.get('phosphorus3'))
#             potassium3 = float(request_data.get('potassium3'))
#             posology3 = float(request_data.get('posology3'))
#             diseasesabnormalities = str(request_data.get('diseasesabnormalities'))
#             diseasesabnormalitiesdate = dt.datetime.strptime(request_data.get('diseasesabnormalitiesdate'), '%Y-%m-%d').date()
#             treatmentobservation = str(request_data.get('treatmentobservation'))
            
#             print(crop.id,croptype1,sowdate1,harvestdate1,product_obtained,nitrogen1,phosphorus1,potassium1,posology1,nitrogen2,phosphorus2,potassium2,posology2,nitrogen3,phosphorus3,potassium3,posology3,diseasesabnormalities,diseasesabnormalitiesdate,treatmentobservation)
#             hist = HistoricFarmland(current_farm_id = crop.id,
#                     		croptype_id = croptype1,
#                     		sow_date = sowdate1,
#                     		harvest_date = harvestdate1,
#                     		product_obtained = product_obtained,
#                     		nitrogen_type1 = nitrogen1,
#                     		phosphorus_type1 = phosphorus1,
#                     		potassium_type1 = potassium1,
#                     		posology_type1 = posology1,
#                     		nitrogen_type2 = nitrogen2,
#                     		phosphorus_type2 = phosphorus2,
#                     		potassium_type2 = potassium2,
#                     		posology_type2 = posology2,
#                     		nitrogen_type3 = nitrogen3,
#                     		phosphorus_type3 = phosphorus3,
#                     		potassium_type3 = potassium3,
#                     		posology_type3 = posology3,
#                     		diseases_abnormalities = diseasesabnormalities,
#                     		diseases_abnormalitiesdate = diseasesabnormalitiesdate,
#                     		observation = treatmentobservation)
#             db.session.add(hist)
#             db.session.commit()
#         if(soil_flag=="Yes"):
#             # farm_id = 1
#             soilsampledate = dt.datetime.strptime(request_data.get('soilsampledate'), '%Y-%m-%d').date()
#             depth = float(request_data.get('depth'))
#             organicmatterlevel = float(request_data.get('organicmatterlevel'))
#             phosphorus_1 = float(request_data.get('phosphorus_1'))
#             phosphorus_2 = float(request_data.get('productobtained'))
#             potassium_1 = float(request_data.get('phosphorus_2'))
#             potassium_2 = float(request_data.get('potassium_2'))
#             calcium_1 = float(request_data.get('calcium_1'))
#             calcium_2 = float(request_data.get('calcium_2'))
#             sand = float(request_data.get('sand'))
#             slit = float(request_data.get('slit'))
#             clay = float(request_data.get('clay'))
#             sulfur = float(request_data.get('sulfur'))
#             magnesium = float(request_data.get('magnesium'))
#             boron = float(request_data.get('boron'))
#             copper = float(request_data.get('copper'))
#             zinc = float(request_data.get('zinc'))
#             manganese = float(request_data.get('manganese'))
            
#             print(crop.id, soilsampledate,depth,organicmatterlevel,phosphorus_1,phosphorus_2,potassium_1,potassium_2,calcium_1,calcium_2,sand,slit,clay,sulfur,magnesium,boron,copper,zinc,manganese)
#             soiltest = SoilFarmland(current_farm_id = crop.id,
#                                     soil_date = soilsampledate,
#                                     soil_depth = depth,
#                                     soil_organic_level = organicmatterlevel,
#                                     phosphorus_ppm = phosphorus_1,
#                                     phosphorus_mg = phosphorus_2,
#                                     potassium_cmolc = potassium_1,
#                                     potassium_mg = potassium_2,
#                                     calcium_cmolc = calcium_1,
#                                     calcium_mg = calcium_2,
#                                     sand = sand,
#                                     slit = slit,
#                                     clay = clay,
#                                     sulfur = sulfur,
#                                     magnesium = magnesium,
#                                     boron = boron,
#                                     copper = copper,
#                                     zinc = zinc,
#                                     manganese = manganese)
#             db.session.add(soiltest)
#             db.session.commit()
            
#         flash('A New Crop Field has been Registered', 'success')
#         return redirect(url_for('main.login'))
#     return render_template('crop2.html', title='Insert a New Crop Field', form=form)



# @main.route("/historic", methods=['GET','POST'])
# @login_required
# def historical():
#     form = HistoricalForm()
#     form.current_farm.choices = [(f.id, f.name) for f in Farmland.query.order_by(Farmland.name).filter(Farmland.harvest_date > dt.date(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)).all()]
#     form.historical_farm.choices = [(f.id, f.name) for f in Farmland.query.order_by(Farmland.name).filter(Farmland.harvest_date <= dt.date(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)).all()]
    
#     Current_Farmland = aliased(Farmland)
#     Historical_Farmland = aliased(Farmland)
    
#     # current_table = db.session.query(Current_Farmland) \
#     #     .order_by(Current_Farmland.name) \
#     #     .filter(Current_Farmland.harvest_date > dt.date(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)) #.all()
    
    
#     # SQLAlchemy query for joining the historical tables with farmland
#     historic_table = db.session.query(Historical, Historical_Farmland, Current_Farmland) \
#         .join(Historical_Farmland, Historical_Farmland.id == Historical.historical_farm_id) \
#         .join(Current_Farmland, Current_Farmland.id == Historical.current_farm_id) \
#         .add_columns(Current_Farmland.name.label('current_name'), 
#                      Historical_Farmland.name.label('historic_name'), 
#                      Current_Farmland.sow_date.label('current_sow_date'), 
#                      Historical_Farmland.sow_date.label('historic_sow_date'), 
#                      Current_Farmland.harvest_date.label('current_harvest_date'), 
#                      Historical_Farmland.harvest_date.label('historic_harvest_date'), 
#                      Current_Farmland.product_expected.label('current_production'), 
#                      Historical_Farmland.product_expected.label('historic_production'),
#                      Historical.product_obtained.label('production_obtained')) # .all()
#     # Equivalent sql query:
#     # historic_table = select a.name as "current_name", 
#     #                     	b.name as "historic_name", 
#     #                     	a.sow_date as "current_sow_date", 
#     #                     	b.sow_date as "historic_sow_date",
#     #                     	a.harvest_date as "current_harvest_date", 
#     #                     	b.harvest_date as "historic_harvest_date", 
#     #                     	a.product_expected as "current_production",
#     #                     	b.product_expected as "historic_production" 
#     #                     from historical as h 
#     #                     join farmlands as a on a.id = h.current_farm 
#     #                     join farmlands as b on b.id = h.historical_farm;
    
#     if form.validate_on_submit():
#         pos = Historical(current_farm_id = form.current_farm.data,
#                          historical_farm_id = form.historical_farm.data,
#                          product_obtained = form.productobtained.data)
#         db.session.add(pos)
#         db.session.commit()
#         flash('A historical farmland was assigned to a current one.', 'success')
#         return redirect(url_for('main.login'))
#     return render_template('historical.html', title='Historical', form=form, historics=historic_table)
