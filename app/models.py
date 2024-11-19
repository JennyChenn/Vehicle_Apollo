from .database import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    #create column for each attribute of the vehicle with elimination of null values
    manufacturer_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    horse_power = db.Column(db.Integer, nullable=False)
    model_name = db.Column(db.String, nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    fuel_type = db.Column(db.String, nullable=False)
    vin = db.Column(db.String, primary_key=True, unique=True, nullable=False)
