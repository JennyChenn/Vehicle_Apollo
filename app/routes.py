from flask import Blueprint, jsonify, request
from .models import Vehicle
from .database import db
from sqlalchemy.exc import IntegrityError #For violation of database constraints


bp = Blueprint('vehicle', __name__)
#crud operation

#for testing the server connection, if the server is working then we will see it's working!! on the first page 
@bp.route('/')
def home():
    return "it's working!!"

@bp.route('/vehicle', methods=['GET'])
def get_vehicles():
    with db.session() as session:
        vehicles = session.query(Vehicle).all()
    return jsonify([vehicle_to_dict(v) for v in vehicles]), 200

#create
#get jsonified data, and add to session, then commit to database
#have a try, catch for handling errors 
@bp.route('/vehicle', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    if data is None or not isinstance(data, dict):
        return jsonify({'error': 'Invalid or missing JSON payload'}), 400
    # check if fields are all there 
    required_fields = ['vin', 'manufacturer_name', 'description', 'horse_power', 'model_name', 'model_year', 'purchase_price', 'fuel_type']
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({'error': f'Field "{field}" is null'}), 422

    try:
        vehicle = Vehicle(**data)
        db.session.add(vehicle)
        db.session.commit()
        return jsonify(vehicle_to_dict(vehicle)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'A vehicle with this VIN already exists'}), 422
    except Exception as e:
        return jsonify({'error': 'Invalid data or internal error'}), 422
    

#read
@bp.route('/vehicle/<string:vin>', methods=['GET'])
def get_vehicle(vin):
    with db.session() as session:
        vehicle = session.get(Vehicle, vin)

    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    return jsonify(vehicle_to_dict(vehicle)), 200


#update 
@bp.route('/vehicle/<string:vin>', methods=['PUT'])
def update_vehicle(vin):
    data = request.get_json()
    if data is None or not isinstance(data, dict):
        return jsonify({'error': 'Invalid or missing JSON payload'}), 400
    with db.session() as session:
        vehicle = session.get(Vehicle, vin)

    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    
    for key, value in data.items():
        if value is None:
            return jsonify({'error': f'Field "{key}" is null'}), 422
        setattr(vehicle, key, value)

    try:
        db.session.commit()
        return jsonify(vehicle_to_dict(vehicle)), 200
    
    except Exception:
        #undo commit
        db.session.rollback()
        return jsonify({'error': 'Invalid data or internal error'}), 422



#delete
@bp.route('/vehicle/<string:vin>', methods=['DELETE'])
def delete_vehicle(vin):
    with db.session() as session:
        vehicle = session.get(Vehicle, vin)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return '', 204

#make all info of vehicle as dictionary so its easier to jsonify
def vehicle_to_dict(vehicle):
    return {
        'vin': vehicle.vin,
        'manufacturer_name': vehicle.manufacturer_name,
        'description': vehicle.description,
        'horse_power': vehicle.horse_power,
        'model_name': vehicle.model_name,
        'model_year': vehicle.model_year,
        'purchase_price': vehicle.purchase_price,
        'fuel_type': vehicle.fuel_type
    }
