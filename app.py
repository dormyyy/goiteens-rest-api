from flask import Flask
from flask_cors import CORS
from celery import Celery
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
ma = Marshmallow(app)
CORS(app, supports_credentials=True, allow_headers=True)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

db = create_engine('postgresql+psycopg2://sodbnphbknvlbt:aab7a821e78002b81bbafb105a794b325d2f2f3a0031c8acea2904a655addcd6@ec2-52-51-3-22.eu-west-1.compute.amazonaws.com:5432/dalie8clvfiean')
base = declarative_base()

Session = sessionmaker(db)
session = Session()


@app.cli.command('db_create')
def db_create():
    base.metadata.create_all(db)
    print('Database created')


@app.cli.command('db_drop')
def db_drop():
    base.metadata.drop_all(db)
    print('Database dropped')


import main
import routes.managers
import routes.users
import routes.statuses
import routes.slots
import routes.groups
import routes.courses
import routes.results
import routes.appointments
import routes.roles
import routes.work_weeks
import routes.manager_plan
import routes.manager_work
import routes.confirmator
import routes.caller
import routes.actions
import routes.superadministrator

if __name__ == '__main__':
    app.run(debug=True)

