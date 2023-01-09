from flask import render_template, url_for, flash, redirect, request
from WebApp import app, db, bcrypt
from WebApp.forms import RegistrationForm, LoginForm, RegistrationPositionForm
from WebApp.models import User, Position
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

lands = (
        ("ID 1", "Nombre 1", "Tipo 1", "Superficie 1", "Ciudad 1"),
        ("ID 2", "Nombre 2", "Tipo 2", "Superficie 2", "Ciudad 2"),
        ("ID 3", "Nombre 3", "Tipo 3", "Superficie 3", "Ciudad 3"),
)

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

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

@app.route("/", methods=['GET', 'POST'])
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