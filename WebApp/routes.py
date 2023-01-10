from flask import render_template, url_for, flash, redirect, request
from WebApp import app, db, bcrypt
from WebApp.forms import RegistrationForm, LoginForm, RegistrationPositionForm, MapForm
from WebApp.models import User, Position
from flask_login import login_user, current_user, logout_user, login_required

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

lands = (
        ("ID 1", "Nombre 1", "Tipo 1", "Superficie 1", "Ciudad 1"),
        ("ID 2", "Nombre 2", "Tipo 2", "Superficie 2", "Ciudad 2"),
        ("ID 3", "Nombre 3", "Tipo 3", "Superficie 3", "Ciudad 3"),
)

@app.route("/")
@app.route("/home")
def home():
     return render_template('home.html', posts=posts)

@app.route("/maps", methods=['GET','POST'])
def maps():
    form = MapForm()
    if request.method == "POST":
        latitude = form.latitude.data
        longitude = form.longitude.data
        return render_template('results.html', title='Maps', lat=latitude , lon=longitude)
    else:
        return render_template('input.html', title='Maps', form=form)

    
    # if request.method == "POST":
    #     lat = request.form["lat"]
    #     lon = request.form["lon"]
    #     return render_template('results.html', lat=lat , lon=lon)
    # else:
    #     return render_template('input.html')

@app.route("/land")
def land_selection():
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
    pos = [(p.id, p.description) for p in Position.query.order_by(Position.description).all()]
    form.position.choices = pos
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, 
                    email = form.email.data, 
                    position_id = form.position.data, 
                    password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Se ha registrado satisfactoriamente', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/registerposition", methods=['GET','POST'])
def registerposition():
    form = RegistrationPositionForm()
    if form.validate_on_submit():
        pos = Position(description = form.description.data)
        db.session.add(pos)
        db.session.commit()
        flash('Se ha registrado una nueva posición', 'success')
        return redirect(url_for('login'))
    return render_template('position.html', title='Position', form=form)


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
            flash('Error al iniciar sesión. Favor verificar el usuario y contraseña', 'danger')
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