from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped')


@app.route('/register', methods=['POST'])
def create_manager():
    name = request.form['name']
    test = Manager.query.filter_by(name=name).first()
    if test:
        return jsonify(message='This manager already exist'), 409
    else:
        manager_name = request.form['name']
        description = request.form['description']
        manager = Manager(name=manager_name, description=description)
        db.session.add(manager)
        db.session.commit()
        return jsonify(message='Manager successfully registered'), 201


@app.route('/remove_manager/<int:manager_id>', methods=['DELETE'])
def remove_manager(manager_id: int):
    manager = Manager.query.filter_by(id=manager_id).first()
    if manager:
        db.session.delete(manager)
        db.session.commit()
        return jsonify(message='Manager successfully deleted.'), 202
    else:
        return jsonify(message='Manager does not exist'), 404


@app.route('/managers', methods=['GET'])
def get_managers():
    managers_list = Manager.query.all()
    result = manager_schema.dump(managers_list)
    return jsonify(data=result)


@app.route('/update/<int:manager_id>', methods=['PUT'])
def update_manager(manager_id: int):
    manager = Manager.query.filter_by(id=manager_id).first()
    if manager:
        manager.name = request.form['name']
        manager.description = request.form['description']
        db.session.commit()
        return jsonify(message=f'Manager {manager.name} successfully updated'), 202
    else:
        return jsonify(message='This manager does not exist.'), 404


# db models
class Manager(db.Model):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(150))


class ManagerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')

manager_schema = ManagerSchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)