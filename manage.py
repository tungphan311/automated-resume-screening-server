import os
import unittest

from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.model import user_model


app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.app_context().push()

mail = Mail(app)
jwt = JWTManager(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()



