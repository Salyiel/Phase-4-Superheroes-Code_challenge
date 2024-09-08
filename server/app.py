#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'



# ----------- Hero Routes -----------
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get_or_404(id)
    return jsonify(hero.to_dict()), 200


@app.route('/heroes', methods=['POST'])
def create_hero():
    data = request.get_json()
    new_hero = Hero(name=data['name'], alias=data['alias'])
    db.session.add(new_hero)
    db.session.commit()
    return jsonify(new_hero.to_dict()), 201


@app.route('/heroes/<int:id>', methods=['PATCH'])
def update_hero(id):
    hero = Hero.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        hero.name = data['name']
    if 'alias' in data:
        hero.alias = data['alias']
    
    db.session.commit()
    return jsonify(hero.to_dict()), 200


@app.route('/heroes/<int:id>', methods=['DELETE'])
def delete_hero(id):
    hero = Hero.query.get_or_404(id)
    db.session.delete(hero)
    db.session.commit()
    return '', 204


# ----------- Power Routes -----------
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers]), 200


@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get_or_404(id)
    return jsonify(power.to_dict()), 200


@app.route('/powers', methods=['POST'])
def create_power():
    data = request.get_json()
    new_power = Power(name=data['name'], description=data['description'])
    db.session.add(new_power)
    db.session.commit()
    return jsonify(new_power.to_dict()), 201


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        power.name = data['name']
    if 'description' in data:
        power.description = data['description']
    
    db.session.commit()
    return jsonify(power.to_dict()), 200


@app.route('/powers/<int:id>', methods=['DELETE'])
def delete_power(id):
    power = Power.query.get_or_404(id)
    db.session.delete(power)
    db.session.commit()
    return '', 204


# ----------- HeroPower Routes -----------
@app.route('/heroes/<int:hero_id>/powers', methods=['POST'])
def assign_power_to_hero(hero_id):
    hero = Hero.query.get_or_404(hero_id)
    data = request.get_json()
    
    new_hero_power = HeroPower(hero_id=hero.id, power_id=data['power_id'], strength=data['strength'])
    db.session.add(new_hero_power)
    db.session.commit()
    
    return jsonify(new_hero_power.to_dict()), 201


@app.route('/heroes/<int:hero_id>/powers', methods=['GET'])
def get_powers_for_hero(hero_id):
    hero = Hero.query.get_or_404(hero_id)
    hero_powers = HeroPower.query.filter_by(hero_id=hero.id).all()
    
    return jsonify([hero_power.to_dict() for hero_power in hero_powers]), 200




if __name__ == '__main__':
    app.run(port=5555, debug=True)
