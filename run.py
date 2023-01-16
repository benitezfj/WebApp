from WebApp import app 

if __name__ == '__main__':
    app.run(debug=True)

# import os
# os.getcwd()
# os.chdir('C:\\Users\\User\\Documents\\Python Scripts\\Web')
# 
# from WebApp import db, app
# app.app_context().push()
# from WebApp.models import User, Role, Farmland
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

# Create a farmland
# cropfiel_1 =  Farmland(croptype_id = 1, sow_date = datetime.date(2022, 12, 1), harvest_date = datetime.date(2023, 12, 1), product_expected =  float(123.45))
# db.session.add(cropfiel_1)
# db.session.commit()
# Farmland.query.all()


# db.drop_all()
# db.create_all()
# Role.query.all()

# sqlite3 site.db
# select * from Role;
# .exit

# import inspect
# lines = inspect.getsource(foo)
# print(lines)