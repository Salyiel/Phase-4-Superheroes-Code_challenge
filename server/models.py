from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # add relationship
    powers = db.relationship('HeroPower', back_populates='hero')

    # add serialization rules
    serialize_rules = ('-powers.hero',)

    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # add relationship
    heroes = db.relationship('HeroPower', back_populates='power')

    # add serialization rules
    serialize_rules = ('-heroes.power',)


    # add validation
    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == '':
            raise ValueError("Power name cannot be empty")
        return name

    @validates('description')
    def validate_description(self, key, description):
        if description and len(description) < 10:
            raise ValueError("Description must be at least 10 characters long")
        return description


    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # add relationships
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # add serialization rules
    hero = db.relationship('Hero', back_populates='powers')
    power = db.relationship('Power', back_populates='heroes')

    # add validation
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['weak', 'strong', 'average']:
            raise ValueError("Invalid strength value")
        return strength


    def __repr__(self):
        return f'<HeroPower {self.id}>'
