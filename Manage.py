from ihome import Create_app_Factroy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ihome import db


app = Create_app_Factroy("dev")
print("app.url_map>>>", app.url_map)

manage = Manager(app)
Migrate(app, db)
manage.add_command("db", MigrateCommand)


if __name__ == '__main__':
	manage.run()

# D:\Flask_Project_Code  activate.bat