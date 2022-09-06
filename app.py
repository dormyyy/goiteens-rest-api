from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 


app = Flask(__name__)
ma = Marshmallow(app)
CORS(app, supports_credentials=True, allow_headers=True)

db = create_engine('postgresql+psycopg2://icdpyzpundpkdf:ff95c34ad1d99630a54ef4bbe3a25226474ca8301eee886dd90191d397150efa@\
ec2-54-228-125-183.eu-west-1.compute.amazonaws.com:5432/d65psvu8kp9m6q')
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