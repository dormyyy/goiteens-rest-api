from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 


app = Flask(__name__)
ma = Marshmallow(app)
CORS(app, supports_credentials=True)

db = create_engine('postgresql+psycopg2://yzgqehdjexidhz:37f052fecbe23a36ae0dcf8f9fcc0522f8bca4364880adb2fb2a2decb4830028@\
ec2-52-30-75-37.eu-west-1.compute.amazonaws.com/dedrifjd2m4iod')
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


if __name__ == '__main__':
    app.run(debug=True)