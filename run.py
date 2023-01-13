from WebApp import app 

if __name__ == '__main__':
    app.run(debug=True)

# import os
# os.getcwd()
# os.chdir('C:\\Users\\Maria\\Documents\\Python Scripts\\Web')
# 
# from WebApp import db, app
# app.app_context().push()
# from WebApp.models import User, Position
# db.create_all()
# position_1 = Position(description = 'Admin')
# position_2 = Position(description = 'Analista')
# position_3 = Position(description = 'Ingeniero')
# db.session.add(position_1)
# db.session.add(position_2)
# db.session.add(position_3)
# db.session.commit()
# Position.query.all()
# position = Position.query.get(1)
# user_1 = User(username='Francisco', email='test@example.com', position_id=position.id)


# db.drop_all()
# db.create_all()
# Position.query.all()

# sqlite3 site.db
# select * from Position;
# .exit

# import inspect
# lines = inspect.getsource(foo)
# print(lines)