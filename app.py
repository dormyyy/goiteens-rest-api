from flask import Flask, jsonify, request
from flask_cors import CORS
from celery import Celery
from flask_marshmallow import Marshmallow
from models import *

app = Flask(__name__)
ma = Marshmallow(app)
CORS(app, supports_credentials=True, allow_headers=True)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.cli.command('db_create')
def db_create():
    base.metadata.create_all(db)
    print('Database created')


@app.cli.command('db_drop')
def db_drop():
    base.metadata.drop_all(db)
    print('Database dropped')


@app.errorhandler(Exception)
def log_exception(e):
    if isinstance(e, Exception):
        status_code = str(e)[:3]
        if status_code.isnumeric():
            if int(status_code) != 500:
                return jsonify(error=str(e)), int(status_code)
            else:
                log = Log(
                    logger=request.endpoint,
                    level='500 ERROR',
                    message=str(e),
                    path=request.path,
                    method=request.method,
                    ip=request.remote_addr
                )
                session.add(log)
                session.commit()
                response = jsonify(error=str(e))
                response.status_code = 400
                return response
        else:
            log = Log(
                logger=request.endpoint,
                level='500 ERROR',
                message=str(e),
                path=request.path,
                method=request.method,
                ip=request.remote_addr
            )
            session.add(log)
            session.commit()
            response = jsonify(error=str(e))
            response.status_code = 400
            return response


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
    app.run(debug=False)

