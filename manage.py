#!/usr/bin/env python

import os
import unittest

from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager, Shell

from consensus_web import create_app, db
from consensus_web.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
#    print(app.root_path)
    os.environ.setdefault("CONSENSUS_UPLOAD_FOLDER", app.root_path+"/data/")
#    print(os.environ.get('CONSENSUS_UPLOAD_FOLDER'))
    manager.run().run(debug=True)