from flask import render_template, url_for, flash, redirect, request
from WebApp import app, db, bcrypt
from WebApp.forms import RegistrationForm, LoginForm, RegistrationRoleForm, MapForm, InsertFarmlandForm, RegistrationCropForm
from WebApp.models import User, Role, Farmland, Crop
from flask_login import login_user, current_user, logout_user, login_required
from earthengine.methods import addDate, getNDVI, getGNDVI, getNDSI, getReCl, getNDWI, getCWSI, get_image_collection_asset
import json
import numpy as np
from datetime import datetime

import folium
import geemap.foliumap as geemap

import ee

ee.Initialize()

posts = [
    {
        ' ': ' ',
        ' ': ' ',
        ' ': ' ',
        ' ': ' '
    }
]

# roi = ee.Geometry.Polygon(-55.04541651090373, -25.45734994544611, 
#                           -55.04445150202754, -25.45709054792545, 
#                           -55.04466969093059, -25.45626820569725, 
#                           -55.04565972074376, -25.45647942106365, 
#                           -55.04541651090373, -25.45734994544611)
roi = ee.Geometry.Polygon(-73.531065,45.136161,
                            -73.497934,45.116298,
                            -73.47167,45.158438,
                            -73.498106,45.174898,
                            -73.531065,45.136161)

roi2 = ee.Geometry.Polygon(-73.490467, 45.180207,
                          -73.447895, 45.159633,
                          -73.435707, 45.172825,
                          -73.476048, 45.191943,
                          -73.490467, 45.180207)

rgbFilter = {'min': 1, 'max': 3000, 'gamma': 1.5, 'bands': ['B4', 'B3', 'B2']}
nrgbFilter = {'min': 1, 'max': 3000, 'gamma': 1.5, 'bands': ['B8', 'B4', 'B3']}
vis = {'min': -1, 'max': 1,
       'palette': [
          '#d73027',
          '#f46d43',
          '#fdae61',
          '#fee08b',
          '#d9ef8b',
          '#a6d96a',
          '#66bd63',
          '#1a9850'
       ]
      }

@app.route("/")
@app.route("/home")
def home():
     return render_template('home.html', posts=posts)











# https://stackoverflow.com/questions/23712986/pre-populate-a-wtforms-in-flask-with-data-from-a-sqlalchemy-object
@app.route("/maps", methods=['GET','POST'])
@login_required
def maps():
    # Farmland.query.get_or_404(id)
    # farmland = Farmland.query
    form = MapForm()
    form.farmland.choices = [(f.id, f.name) for f in Farmland.query.order_by(Farmland.name).all()]
    # lands = [(f.id, f.name) for f in Farmland.query.order_by(Farmland.name).all()]
    if form.validate_on_submit(): 
    # if request.method == "POST":
        farm_id = form.farmland.data
        # print(farm_id)
        index = form.indices.data
        # print(index)
        start_date = form.start_date.data
        start_date = start_date.strftime("%Y-%m-%d")
        # print(start_date)
        end_date = form.end_date.data
        end_date = end_date.strftime("%Y-%m-%d")
        # print(end_date)
        coverage = form.cloud_cover.data
        # print(coverage)
        
        
        lands = Farmland.query.get_or_404(farm_id)
        crop_descrip = lands.crop.description
        # print(crop_descrip)
        harvest_date = lands.harvest_date.strftime("%Y-%m-%d")
        # print(harvest_date)
        sow_date = lands.sow_date.strftime("%Y-%m-%d")
        # print(sow_date)
        product_expected = lands.product_expected
        # print(product_expected)
        coord = np.array(lands.coordinates.split(','))
        # print(coord)
        roi= ee.Geometry.Polygon([float(i) for i in coord])
        lon = ee.Number(roi.centroid().coordinates().get(0)).getInfo();
        lat = ee.Number(roi.centroid().coordinates().get(1)).getInfo();
        # coord = coord.astype(float)
        
        # lands.coordinates
        # lands.coordinates
        # form.coordinates.data = coord.split(','), farm_data.coordinates
        # coord = np.array(coord)
        # coord = coord.astype(float)
        
        # # coord.reshape(4,2).tolist() 4=fila, 2=columnas
        # latitude = form.latitude.data
        # longitude = form.longitude.data
        # Crop = Crop.query.get(lands.croptype_id).description
        # print(form.is_submitted(), "Es submitted?")
        # print(form.validate(), "Es valido?")
        
        
        figure = folium.Figure()
        Map = geemap.Map(center=(lat, lon), zoom = 16, plugin_Draw = False, Draw_export = False, plugin_LayerControl = False)
        Map.add_basemap('HYBRID')

        # get_image_collection_asset()
        # # ----Earth Engine Extraction-----
        # start_date = '2015-06-23'
        # end_date = '2023-01-20'

        # featureCollection = ee.FeatureCollection(json.loads(geo_json))
        print(start_date, "Fecha de inicio")
        print(end_date, "Fecha de fin")
        print(roi)
        print(coverage)
        
        collection =  ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterDate(start_date, end_date) \
            .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',coverage)) \
            .filterBounds(roi) \
            .sort('system:time_start', False) 
            
        if index == 1:
            print("NDVI es calculado.")
            collection = collection.map(addDate).map(getNDVI)
            clipped = collection.map(lambda image: image.clip(roi))
            Map.addLayer(clipped.first().select('NDVI'), vis, 'NDVI')
        elif index == 2:
            print("GNDVI")
            collection = collection.map(addDate).map(getGNDVI)            
            clipped = collection.map(lambda image: image.clip(roi))
            Map.addLayer(clipped.first().select('GNDVI'),vis, 'GNDVI')
        elif index == 3:
            print("NDSI")
            collection = collection.map(addDate).map(getNDSI)
            clipped = collection.map(lambda image: image.clip(roi))
            Map.addLayer(clipped.first().select('NDSI'), vis, 'NDSI')
        elif index == 4:
            print("RECL")
            collection = collection.map(addDate).map(getReCl)
            clipped = collection.map(lambda image: image.clip(roi))
            Map.addLayer(clipped.first().select('ReCl'), vis, 'ReCl')
        elif index == 5:
            print("NDWI")
            collection = collection.map(addDate).map(getNDWI)
            clipped = collection.map(lambda image: image.clip(roi))
            Map.addLayer(clipped.first().select('NDWI'), vis, 'NDWI')
        else: 
            print("CWSI")
            collection = collection.map(addDate).map(getNDVI).map(getNDWI)
            collection = collection.map(getCWSI)
            clipped = collection.map(lambda image: image.clip(roi))
            Map.addLayer(clipped.first().select('CWSI'), vis, 'CWSI')

        # collection = collection.map(addDate).map(getNDVI).map(getGNDVI).map(getNDSI).map(getReCl).map(getNDWI)
        # collection = collection.map(getCWSI)    
        
        # clipped = collection.map(lambda image: image.clip(roi))
        # Map.addLayer(clipped.first(),           nrgbFilter, 'Cetapar Maiz - False RGB')
        # Map.addLayer(clipped.first(),           rgbFilter,  'Cetapar Maiz - RGB')
        # Map.addLayer(clipped.first().select('NDVI'), vis, 'NDVI')
        # Map.addLayer(clipped.first().select('GNDVI'),vis, 'GNDVI')
        # Map.addLayer(clipped.first().select('NDSI'), vis, 'NDSI')
        # Map.addLayer(clipped.first().select('ReCl'), vis, 'ReCl')
        # Map.addLayer(clipped.first().select('CWSI'), vis, 'CWSI')
        Map.addLayer(ee.Image().paint(roi,0,2), {},         'Region of Interest')
        # new_result=imageClipped_2022_08_22.expression('b(24) >= 0.9 ? (200*0.7) : (b(24) >= 0.7 ? (200*1) : (200 * 1.1))').rename('result1')
        Map.add_colorbar(vis, label="Scale", layer_name="SRTM DEM")

        # # Map.centerObject(roi,17)
        # # ---------------------------------
        map_url = get_image_collection_asset(platform='sentinel', sensor='2', product='TOA', cloudy=10, date_from=start_date , date_to=end_date, roi=roi,reducer='median')
        print(map_url)
        Map.add_to(figure)

        # # figure.render()
        return render_template('results2.html', title='Maps', maps=figure.render())
    # else:
    return render_template('input.html', title='Maps', form=form)
 


















@app.route("/farmland", methods=['GET', 'POST'])
@login_required
def insert_farmland_data():
    form = InsertFarmlandForm()
    crops = [(c.id, c.description) for c in Crop.query.order_by(Crop.description).all()]
    form.croptype.choices = crops
    if form.validate_on_submit(): 
        # print(form.is_submitted(), "Es submitted?")
        # print(form.validate(), "Es valido?")
        # print(request.content_type)
        request_data  = request.get_json()
        # print(request_data)
        descrip = request_data['name']
        coord = request_data['coordinates'].replace("[","").replace("]","").replace("\n","").replace(" ","")
        crop = int(request_data['croptype'])
        sow = datetime.strptime(request_data['sowdate'], '%Y-%m-%d').date()
        harvest = datetime.strptime(request_data['harvestdate'], '%Y-%m-%d').date()
        product = float(request_data['productexpected'])
        
        crop = Farmland(name = descrip,
                       croptype_id = crop,
                       sow_date = sow,
                       harvest_date = harvest,
                       coordinates = coord,
                       product_expected = product)
        # crop = Farmland(croptype_id = form.croptype.data,
        #                sow_date = form.sowdate.data,
        #                harvest_date = form.harvestdate.data,
        #                coordinates = coord,
        #                product_expected =  form.productexpected.data)
        
        db.session.add(crop)
        db.session.commit()
        # print("Chauuu")
        flash('A New Crop Field has been Registered', 'success')
        return redirect(url_for('insert_farmland_data'))

    return render_template('crop.html', title='Insert a New Crop Field', form=form)

@app.route("/land")
@login_required
def land_selection():
    # lands = Farmland.query
    # lands = Farmland.query.join(Crop, Farmland.croptype_id==Crop.id).add_columns(Farmland.id, Crop.description, Farmland.sow_date, Farmland.harvest_date, Farmland.product_expected, Farmland.coordinates).filter(Farmland.croptype_id == Crop.id).filter(friendships.user_id == userID).paginate(page, 1, False).all()
    # select a.id, 
             # b.description, 
             # a.sow_date, 
             # a.harvest_date, 
             # a.product_expected, 
             # a.coordinates from farmlands a join crops b on a.croptype_id = b.id;
    lands = db.session.query(Farmland).join(Crop).add_columns(Farmland.id, Farmland.name, Crop.description, Farmland.sow_date, Farmland.harvest_date, Farmland.product_expected, Farmland.coordinates).filter(Farmland.croptype_id == Crop.id)
   
    return render_template('land_selection.html', title='Land', lands=lands)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

# form.position.data = pos
# Position.query.filter_by(id=form.position.data).first()
@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/role", methods=['GET','POST'])
@login_required
def registerrole():
    form = RegistrationRoleForm()
    if form.validate_on_submit():
        pos = Role(description = form.description.data)
        db.session.add(pos)
        db.session.commit()
        flash('A new role has been registered', 'success')
        return redirect(url_for('login'))
    return render_template('position.html', title='Role', form=form)


@app.route("/crop", methods=['GET','POST'])
@login_required
def registercrop():
    form = RegistrationCropForm()
    if form.validate_on_submit():
        pos = Crop(description = form.description.data)
        db.session.add(pos)
        db.session.commit()
        flash('A new crop type has been registered.', 'success')
        return redirect(url_for('login'))
    return render_template('croptype.html', title='Crop', form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')




# import folium
# from folium import plugins
# import geemap.foliumap as geemap
# async def main():   
    # if request.method == "POST":
    #     # Get shops data from OpenStreetMap
    #     shops = get_shops(request.form["lat"], )

    #     # Initialize variables
    #     id_counter = 0
    #     markers = ''
    #     for node in shops.nodes:

    #         # Create unique ID for each marker
    #         idd = 'shop' + str(id_counter)
    #         id_counter += 1

    #         # Check if shops have name and website in OSM
    #         try:
    #             shop_brand = node.tags['brand']
    #         except:
    #             shop_brand = 'null'

    #         try:
    #             shop_website = node.tags['website']
    #         except:
    #             shop_website = 'null'

    #         # Create the marker and its pop-up for each shop
    #         markers += "var {idd} = L.marker([{latitude}, {longitude}]);\
    #                     {idd}.addTo(map).bindPopup('{brand}<br>{website}');".format(idd=idd, latitude=node.lat,\
    #                                                                                  longitude=node.lon,
    #                                                                                  brand=shop_brand,\
    #                                                                                  website=shop_website)

    #     # Render the page with the map
    #     return render_template('results.html', markers=markers, lat=request.form["lat"], lon=request.form["lon"])
    # else:
    #     # Render the input form
    #     return render_template('input.html')
    
    # markers=[
    #     {
    #     'lat':0,
    #     'lon':0,
    #     'popup':'This is the middle of the map.'
    #     }
    # ]
    # return render_template('maps.html',markers=markers)

    # figure = folium.Figure()

    # m = folium.Map(
    #     location=[28.5973518, 83.54495724],
    #     zoom_start=8,
    # )
    # m.add_to(figure)

    # dataset = ee.ImageCollection('MODIS/006/MOD13Q1').filter(ee.Filter.date('2019-07-01', '2019-11-30')).first()
    # modisndvi = dataset.select('NDVI')
    # visParams = {'min':0, 'max':3000, 'palette':['225ea8','41b6c4','a1dab4','034B48']}
    # vis_paramsNDVI = {
    #     'min': 0,
    #     'max': 9000,
    #     'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48',]}

    # map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
    # folium.raster_layers.TileLayer(
    #             tiles = map_id_dict['tile_fetcher'].url_format,
    #             attr = 'Google Earth Engine',
    #             name = 'NDVI',
    #             overlay = True,
    #             control = True
    #             ).add_to(m)

    # m.add_child(folium.LayerControl())
    # return figure.render()


    # start_coords = (46.9540700, 142.7360300)
    # folium_map = folium.Map(location=start_coords, zoom_start=14)
    # return folium_map._repr_html_()

    # figure = folium.Figure()
    # Map = geemap.Map(plugin_Draw = True, Draw_export = True)
    # map2 = Map.add_to(figure)
    # return map2._repr_html_()

    # figure.render()
    # return render_template('maps.html', map=figure)
    # return render_template('maps.html', maps=folium_map)