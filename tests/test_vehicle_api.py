import pytest
from app import create_app, db
from app.models import Vehicle

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Create tables
    
    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()  # Cleanup

def test_create_vehicle(client):
    data = {
        'vin': '1HGCM82633A123456',
        'manufacturer_name': 'Honda',
        'description': 'Compact car',
        'horse_power': 150,
        'model_name': 'Civic',
        'model_year': 2020,
        'purchase_price': 20000.00,
        'fuel_type': 'Petrol'
    }
    response = client.post('/vehicle', json=data)
    assert response.status_code == 201
    assert response.get_json().get('vin') == data['vin']

def test_get_all_vehicles(client):
    vehicles = [
        {'vin': '1HGCM82633A123456', 'manufacturer_name': 'Honda', 'description': 'Compact car', 'horse_power': 150, 'model_name': 'Civic', 'model_year': 2020, 'purchase_price': 20000.00, 'fuel_type': 'Petrol'},
        {'vin': '2HGCM82633A654321', 'manufacturer_name': 'Toyota', 'description': 'Sedan', 'horse_power': 180, 'model_name': 'Camry', 'model_year': 2021, 'purchase_price': 25000.00, 'fuel_type': 'Gasoline'}
    ]
    for vehicle in vehicles:
        client.post('/vehicle', json=vehicle)

    response = client.get('/vehicle')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == len(vehicles)
    assert data[0]['vin'] == vehicles[0]['vin']
    assert data[1]['vin'] == vehicles[1]['vin']

def test_get_vehicle_by_vin(client):
    client.post('/vehicle', json={'vin': '4HGCM82633A111111', 'manufacturer_name': 'Nissan', 'description': 'Truck', 'horse_power': 300, 'model_name': 'Frontier', 'model_year': 2023, 'purchase_price': 40000.00, 'fuel_type': 'Gasoline'})
    response = client.get('/vehicle/4HGCM82633A111111')
    assert response.status_code == 200
    assert response.get_json().get('vin') == '4HGCM82633A111111'

def test_put_update_vehicle(client):
    client.post('/vehicle', json={'vin': '5HGCM82633A222222', 'manufacturer_name': 'Chevrolet', 'description': 'Compact', 'horse_power': 160, 'model_name': 'Malibu', 'model_year': 2019, 'purchase_price': 23000.00, 'fuel_type': 'Hybrid'})
    response = client.put('/vehicle/5HGCM82633A222222', json={'description': 'Updated compact car', 'horse_power': 170, 'model_year': 2020})
    assert response.status_code == 200
    data = response.get_json()
    assert data['description'] == 'Updated compact car'
    assert data['horse_power'] == 170

def test_delete_vehicle(client):
    client.post('/vehicle', json={'vin': '6HGCM82633A333333', 'manufacturer_name': 'BMW', 'description': 'Luxury SUV', 'horse_power': 350, 'model_name': 'X5', 'model_year': 2021, 'purchase_price': 60000.00, 'fuel_type': 'Petrol'})
    response = client.delete('/vehicle/6HGCM82633A333333')
    assert response.status_code == 204
    response = client.get('/vehicle/6HGCM82633A333333')
    assert response.status_code == 404

def test_create_vehicle_missing_required_fields(client):
    response = client.post('/vehicle', json={'manufacturer_name': 'Honda', 'description': 'Compact car', 'horse_power': 150, 'model_name': 'Civic', 'model_year': 2020, 'purchase_price': 20000.00, 'fuel_type': 'Petrol'})
    assert response.status_code == 422
    assert 'Field "vin" is null' in response.get_json().get('error')

def test_create_vehicle_with_null_fields(client):
    response = client.post('/vehicle', json={'vin': '7HGCM82633A444444', 'manufacturer_name': None, 'description': 'Compact car', 'horse_power': 150, 'model_name': 'Accord', 'model_year': 2021, 'purchase_price': 25000.00, 'fuel_type': 'Gasoline'})
    assert response.status_code == 422
    assert 'Field "manufacturer_name" is null' in response.get_json().get('error')

# def test_update_vehicle_invalid_json(client):
#     client.post('/vehicle', json={'vin': '8HGCM82633A555555', 'manufacturer_name': 'Toyota', 'description': 'Sedan', 'horse_power': 200, 'model_name': 'Camry', 'model_year': 2022, 'purchase_price': 30000.00, 'fuel_type': 'Petrol'})
#     response = client.put('/vehicle/8HGCM82633A555555', data="Invalid JSON", content_type='application/json')
#     assert response.status_code == 400
#     assert 'error' in response.get_json()

def test_update_vehicle_with_null_fields(client):
    client.post('/vehicle', json={'vin': '9HGCM82633A666666', 'manufacturer_name': 'Ford', 'description': 'SUV', 'horse_power': 250, 'model_name': 'Explorer', 'model_year': 2020, 'purchase_price': 35000.00, 'fuel_type': 'Diesel'})
    response = client.put('/vehicle/9HGCM82633A666666', json={'manufacturer_name': None})
    assert response.status_code == 422
    assert 'Field "manufacturer_name" is null' in response.get_json().get('error')

def test_create_duplicate_vehicle(client):
    client.post('/vehicle', json={'vin': '1HGCM82633A777777', 'manufacturer_name': 'Chevrolet', 'description': 'Truck', 'horse_power': 300, 'model_name': 'Silverado', 'model_year': 2023, 'purchase_price': 45000.00, 'fuel_type': 'Diesel'})
    response = client.post('/vehicle', json={'vin': '1HGCM82633A777777', 'manufacturer_name': 'Chevrolet', 'description': 'Truck', 'horse_power': 300, 'model_name': 'Silverado', 'model_year': 2023, 'purchase_price': 45000.00, 'fuel_type': 'Diesel'})
    assert response.status_code == 422
    assert 'A vehicle with this VIN already exists' in response.get_json().get('error')
