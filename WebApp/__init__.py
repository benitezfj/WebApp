from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from WebApp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
            
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        from WebApp.models import User, Role, Farmland, Crop, HistoricFarmland, SoilFarmland
        db.create_all()
    
    # app.config['SECRET_KEY'] = 'ec8466a71d3153c8f7adfb411dffdc47f7adfb411dffdc47'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    from WebApp.routes import main
    app.register_blueprint(main)
    
    return app

    