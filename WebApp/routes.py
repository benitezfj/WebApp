from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import aliased
from WebApp import db, bcrypt
from WebApp.forms import RegistrationForm, LoginForm, RegistrationRoleForm, MapForm, InsertFarmlandForm, RegistrationCropForm, HistoricalForm, FertilizarMapForm
from WebApp.models import User, Role, Farmland, Crop, Historical
from fertilizer.calculator_spinach import spinachFertilizer
from fertilizer.fertilizerCalculator import fertilizerCalculator
from earthengine.methods import get_image_collection_asset, get_fertilizer_map

import numpy as np
import datetime as dt
import ee

# earthengine authenticate
ee.Initialize()
# from WebApp.config import Config
# EE_CREDENTIALS = ee.ServiceAccountCredentials(config.EE_ACCOUNT, config.EE_PRIVATE_KEY_FILE)
# ee.Initialize(EE_CREDENTIALS)

main = Blueprint('main', __name__)


posts = [
    {
        ' ': ' ',
        ' ': ' ',
        ' ': ' ',
        ' ': ' '
    }
]

@main.route("/")
@main.route("/home")
def home():
     return render_template('home.html', posts=posts)


@main.route("/maps", methods=['GET','POST'])
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
        # print(map_url)
        # print(index_name)
        # Map.add_to(figure)
        # list_index = [(1, 'NDVI'), (2, 'GNDVI'), (3, 'NDSI'), (4, 'RECL'), (5, 'NDWI'), (6, 'CWSI')]
        # list_index = list_index[index-1][1]
        
        map_json = {'map_url': map_url, 
                    'latitude': lat, 
                    'longitude': lon,
                    'farmland_name': farmland_name,
                    'index_name': index_name,
                    'indexdate': end_date,
                    'cover': coverage}    
        
        # map_json = json.dumps(map_json)
        # print(map_json)
        
        # return render_template('results2.html', title='Maps', maps=figure.render())
        return render_template('results.html', title='Maps', maps=map_json, form=form)
    # else:
    return render_template('input.html', title='Maps', form=form) 




@main.route("/fertilizer", methods=['GET','POST'])
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
        
        # for index, value in np.ndenumerate(fertilizer_measure):
        #     if index[1] == 0:
        #         if fertilizer_measure[index] >= 0.9:
        #             fertilizer_measure[index] = fertilizer_measure[index] * 0.9
        #         elif fertilizer_measure[index] >= 0.7:
        #             fertilizer_measure[index] = fertilizer_measure[index] * 1
        #         else: 
        #             fertilizer_measure[index] = fertilizer_measure[index] * 1.1

        # Extract amount of fertilizer kg/ha
        amount_fertilizer = []
        for index, value in np.ndenumerate(fertilizer_measure):
                    if index[1] == 0:
                        amount_fertilizer.append(value)
        # NPK Commercial
        type_fertilizer = np.delete(fertilizer_measure, 0, axis=1).astype(int)
        
        fertilizer = []
        fertilizer.append(production_exp)
        # fertilizer.append(fertilizer_measure)
        fertilizer.append(amount_fertilizer)
        fertilizer.append(type_fertilizer)
        fertilizer.append(diff_blend)
        print(fertilizer)
        
        # print(nitrogen, potassium, phosphorus)
        # print(a)
        # print(b)
        # for i in range(len(a)):
        #     print(f'{a[i][0]}', 'kg/ha of', f'{a[i][1]}- {a[i][2]}- {a[i][3]}-')
   
            
        # print('\nDifference from desired blend:', f'{b[0]}-, {b[1]}-, {b[2]}-')
            
        # input_1 = input('Please enter first floating point value:\n')
        # input_1 = float(input_1)
        
        # input_2 = input('Please enter second floating point value:\n')
        # input_2 = float(input_2)
        
        # print(f'Sum of {input_1} and {input_2} is {input_1+input_2}')
        
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
                    # 'cover': coverage}    
        
        print(map_json)
        print(f'{nutrients[0]} kg/ha of {nutrients[1]}- {nutrients[2]}- {nutrients[3]}-')
        return render_template('results_fertilizer.html', title='Maps', maps=map_json, form=form, nutrient=nutrients, fertilizer_measure = fertilizer)
    return render_template('input_fertilizer.html', title='Maps', form=form)











@main.route("/historic", methods=['GET','POST'])
@login_required
def historical():
    form = HistoricalForm()
    form.current_farm_id.choices = [(f.id, f.name) for f in Farmland.query.order_by(Farmland.name).filter(Farmland.harvest_date > dt.date(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)).all()]
    form.historical_farm_id.choices = [(f.id, f.name) for f in Farmland.query.order_by(Farmland.name).filter(Farmland.harvest_date <= dt.date(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day)).all()]
    
    Current_Farmland = aliased(Farmland)
    Historical_Farmland = aliased(Farmland)
    
    # SQLAlchemy query for joining the historical tables with farmland
    historic_table = db.session.query(Historical, Historical_Farmland, Current_Farmland) \
        .join(Historical_Farmland, Historical_Farmland.id == Historical.historical_farm_id) \
        .join(Current_Farmland, Current_Farmland.id == Historical.current_farm_id) \
        .add_columns(Current_Farmland.name.label('current_name'), 
                     Historical_Farmland.name.label('historic_name'), 
                     Current_Farmland.sow_date.label('current_sow_date'), 
                     Historical_Farmland.sow_date.label('historic_sow_date'), 
                     Current_Farmland.harvest_date.label('current_harvest_date'), 
                     Historical_Farmland.harvest_date.label('historic_harvest_date'), 
                     Current_Farmland.product_expected.label('current_production'), 
                     Historical_Farmland.product_expected.label('historic_production'),
                     Historical.product_obtained.label('production_obtained')) # .all()
    # Equivalent sql query:
    # historic_table = select a.name as "current_name", 
    #                     	b.name as "historic_name", 
    #                     	a.sow_date as "current_sow_date", 
    #                     	b.sow_date as "historic_sow_date",
    #                     	a.harvest_date as "current_harvest_date", 
    #                     	b.harvest_date as "historic_harvest_date", 
    #                     	a.product_expected as "current_production",
    #                     	b.product_expected as "historic_production" 
    #                     from historical as h 
    #                     join farmlands as a on a.id = h.current_farm_id 
    #                     join farmlands as b on b.id = h.historical_farm_id;
    
    if form.validate_on_submit():
        pos = Historical(current_farm_id = form.current_farm_id.data,
                         historical_farm_id = form.historical_farm_id.data,
                         product_obtained = form.productobtained.data)
        db.session.add(pos)
        db.session.commit()
        flash('A historical farmland was assigned to a current one.', 'success')
        return redirect(url_for('main.login'))
    return render_template('historical.html', title='Historical', form=form, historics=historic_table)


@main.route("/farmland", methods=['GET', 'POST'])
@login_required
def insert_farmland_data():
    form = InsertFarmlandForm()
    crops = [(c.id, c.description) for c in Crop.query.order_by(Crop.description).all()]
    form.croptype.choices = crops
    if form.validate_on_submit(): 
        request_data = request.get_json()
        # descrip = request_data['name']
        descrip = request_data.get('name')
        # coord = request_data['coordinates'].replace("[","").replace("]","").replace("\n","").replace(" ","")
        coord = request_data.get('coordinates').replace("[","").replace("]","").replace("\n","").replace(" ","")
        # crop = int(request_data['croptype'])
        crop = int(request_data.get('croptype'))
        # sow = dt.datetime.strptime(request_data['sowdate'], '%Y-%m-%d').date()
        sow = dt.datetime.strptime(request_data.get('sowdate'), '%Y-%m-%d').date()
        # harvest = dt.datetime.strptime(request_data['harvestdate'], '%Y-%m-%d').date()
        harvest = dt.datetime.strptime(request_data.get('harvestdate'), '%Y-%m-%d').date()
        # product = float(request_data['productexpected'])
        product = float(request_data.get('productexpected'))
        crop = Farmland(name = descrip,
                       croptype_id = crop,
                       sow_date = sow,
                       harvest_date = harvest,
                       coordinates = coord,
                       product_expected = product)
        
        db.session.add(crop)
        db.session.commit()
        flash('A New Crop Field has been Registered', 'success')
        # return redirect(url_for('main.insert_farmland_data'))
        return redirect(url_for('main.home'))
    return render_template('crop.html', title='Insert a New Crop Field', form=form)


@main.route("/list")
@login_required
def land_selection():
    lands = db.session.query(Farmland).join(Crop).add_columns(Farmland.id, Farmland.name, Crop.description, Farmland.sow_date, Farmland.harvest_date, Farmland.product_expected, Farmland.coordinates).filter(Farmland.croptype_id == Crop.id)
    return render_template('land_selection.html', title='Land', lands=lands)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


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


@main.route("/role", methods=['GET','POST'])
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


@main.route("/crop", methods=['GET','POST'])
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


