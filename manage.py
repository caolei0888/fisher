from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.models.base import db
from fisher import app

# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = 'mysql+cymysql://root:123456@localhost/fisher'



migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
