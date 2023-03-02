from WebApp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)



# import os
# os.getcwd()
# os.chdir('C:\\Users\\User\\Documents\\Python Scripts\\Web')
# 
# from WebApp import db, create_app
# app = create_app()
# app.app_context().push()
# from WebApp.models import User, Role, HistoricFarmland, SoilFarmland, Unit, Farmland, Crop
# db.create_all()

# Create three roles
# role_1 = Role(description = 'Admin')
# role_2 = Role(description = 'Analista')
# role_3 = Role(description = 'Ingeniero')
# db.session.add(role_1)
# db.session.add(role_2)
# db.session.add(role_3)
# db.session.commit()
# Role.query.all()
# role = Role.query.get(1)
# user_1 = User(username='User_1', email='test@example.com', role_id=role.id)

# Create nine roles
# crop_1 = Crop(description = 'Soja')
# crop_2 = Crop(description = 'Maiz')
# crop_3 = Crop(description = 'Trigo')
# crop_4 = Crop(description = 'Oliva')
# crop_5 = Crop(description = 'Arroz')
# crop_6 = Crop(description = 'Fruta')
# crop_7 = Crop(description = 'Raices y Tuberculos')
# crop_8 = Crop(description = 'Vegetales')
# crop_9 = Crop(description = 'Azucar')

# db.session.add(crop_1)
# db.session.add(crop_2)
# db.session.add(crop_3)
# db.session.add(crop_4)
# db.session.add(crop_5)
# db.session.add(crop_6)
# db.session.add(crop_7)
# db.session.add(crop_8)
# db.session.add(crop_9)

# db.session.commit()
# Crop.query.all()
# crop = Crop.query.get(1)

# Create three unit
# unit_1 = Unit(description = 'ppm')
# unit_2 = Unit(description = 'mg/dm3')
# unit_3 = Unit(description = 'cmolc/dm3')

# db.session.add(unit_1)
# db.session.add(unit_2)
# db.session.add(unit_3)
# db.session.commit()


# Create a farmland
# cropfiel_1 =  Farmland(croptype_id = 1, sow_date = datetime.date(2022, 12, 1), harvest_date = datetime.date(2023, 12, 1), product_expected =  float(123.45))
# db.session.add(cropfiel_1)
# db.session.commit()
# Farmland.query.all()
# Farmland.query.filter_by(id=1).first()

# db.drop_all()
# db.create_all()
# Role.query.all()

# sqlite3 site.db
# select * from Role;
# .exit

# import inspect
# lines = inspect.getsource(foo)
# print(lines)
# HistoricFarmland.__table__.drop()
# DELETE FROM tables;