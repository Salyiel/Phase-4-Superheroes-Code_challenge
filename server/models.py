from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Configure metadata for naming conventions
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize the database
db = SQLAlchemy(metadata=metadata)

# Hero model
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    # One-to-many relationship with HeroPower
    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')
    
    # Association proxy to access related powers through hero_powers
    powers = association_proxy('hero_powers', 'power')

    # Serialization rules
    serialize_rules = ('-hero_powers.hero', '-powers.heroes')

    def __repr__(self):
        return f'<Hero {self.id} {self.name}>'

# Power model
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)

    # One-to-many relationship with HeroPower
    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')
    
    # Association proxy to access related heroes through hero_powers
    heroes = association_proxy('hero_powers', 'hero')

    # Serialization rules
    serialize_rules = ('-hero_powers.power', '-heroes.powers')

    # Validation for name and description
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 3:
            raise ValueError("Power name must be at least 3 characters long.")
        return name

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 10:
            raise ValueError("Description must be at least 10 characters long.")
        return description

    def __repr__(self):
        return f'<Power {self.id} {self.name}>'

# HeroPower model (join table)
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # Foreign keys to Hero and Power models
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # Relationships
    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    # Serialization rules
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    # Validation for strength
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of: Strong, Weak, or Average.")
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id} Hero: {self.hero_id} Power: {self.power_id} Strength: {self.strength}>'