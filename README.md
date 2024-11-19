# Vehicle CRUD Web Service

Project Overview

This project implements a simple CRUD-style(create, read, update, delete) web service for managing vehicles using Flask and SQLAlchemy. The reasons why that I used SQLAlchemy is that after research I found that the Flask-SQLAlchemy extension makes database configuration easier. The service provides API endpoints to create, read, update, and delete vehicle records stored in a database.

Project Setup

1. Initial Setup
- Created Project Structure:
  - Created a project directory named `Vehicle_Apollo`.
  - Created subdirectories and files:
    Vehicle_Apollo/
    ├── app/
    │   ├── __init__.py            # Initializes the Flask application and registers routes
    │   ├── database.py            # Sets up SQLAlchemy database connection
    │   ├── models.py              # Defines the Vehicle with attributes
    │   ├── routes.py              # Implements API routes for CRUD operations
    ├── run.py                     # run to start Flask 
    ├── requirements.txt           # Project dependencies, packages
    ├── README.md                  # Project overview and documentation
    └── tests/
        └── test_vehicle_api.py    # Unit tests for the API

- Initialized Git Repository:
  - Run command `git init` to initialize a local Git repository.
  - Added and committed initial files.

2. Virtual Environment
- Created Virtual Environment:
  - Created a virtual environment using:
    python3 -m venv venv

  - Activated the virtual environment:
    - On macOS/Linux:
      source venv/bin/activate
   
    - On Windows:
      venv\Scripts\activate

- Installed Dependencies:
    pip install Flask SQLAlchemy pytest
  - Created `requirements.txt`:
    pip freeze > requirements.txt - automatically record all the packages and dependencies version in the requirements.txt file
  

3. Database and Models
- Defined the `Vehicle` Model in `app/models.py` using SQLAlchemy with fields:
  - `vin` (unique, case-insensitive, primary key)
  - `manufacturer_name`, `description`, `horse_power`, `model_name`, `model_year`, `purchase_price`, and `fuel_type`.

4. API Routes
- Implemented CRUD API Endpoints in `app/routes.py`:
  - `GET /vehicle`: Retrieve all vehicles.
  - `POST /vehicle`: Create a new vehicle record.
  - `GET /vehicle/{vin}`: Retrieve a given vehicle by VIN.
  - `PUT /vehicle/{vin}`: Update an existing vehicle by VIN.
  - `DELETE /vehicle/{vin}`: Delete a vehicle by VIN.

5. Application Entry Point
- Created `run.py` to initialize and run the Flask application, run command: 'python3 run.py' in a new terminal in the folder directory to start the server. In this case, the server is hosted on http://127.0.0.1:5000


Challenges Faced

1. Database Connection Issues
- Problem: Initially, I encountered issues with setting up and initializing the SQLite database.
- Solution: Ensured `SQLAlchemy` was correctly initialized in `app/database.py` and verified the database URI configuration in `app/__init__.py`.

2. Handling Unique Constraints
- Problem: Ensuring that VIN is unique (case-insensitive) required careful validation.
- Solution: Added validation logic to handle unique constraint violations gracefully and provided meaningful error responses.

3. Error Handling for Invalid Requests
- Problem: Managing different error responses for malformed JSON requests and validation errors.
- Solution: Implemented error handling logic to return appropriate status codes (`400 Bad Request`, `422 Unprocessable Entity`) with informative messages.

4. Testing Environment Issues
- Problem: Encountered a `ModuleNotFoundError` when trying to run tests using `pytest`, indicating that the `app` module could not be found by the test file.
- Solution:
  - Verified the directory structure and ensured `app/` contained an `__init__.py` file, making it a package.
  - Ensured the `PYTHONPATH` was correctly set by running `pytest` with `PYTHONPATH=.`.
  - Made sure to run `pytest` from the project root directory.
  - Added and adjusted imports to use absolute paths, e.g., `from app import create_app, db`.
  - Verified that the test files and functions were correctly named to be discovered by `pytest`.
  - Ultimately resolved the issue by ensuring the correct structure, `PYTHONPATH`, and function naming conventions for `pytest`.

Testing

Unit Tests
- Created unit tests in `tests/test_vehicle_api.py` using `pytest`.
- Tests Include:
  - Testing all CRUD operations (`GET`, `POST`, `PUT`, `DELETE`) for the `/vehicle` endpoint.
  - Validating responses for malformed requests and missing fields.
Tests Running Commands:
- run command: 'pytest' in a new terminal




### 3. Data Model
- **Vehicle Table**:
  - `vin` (string, primary key, unique)
  - `manufacturer_name` (string)
  - `description` (string)
  - `horse_power` (integer)
  - `model_name` (string)
  - `model_year` (integer)
  - `purchase_price` (decimal)
  - `fuel_type` (string)

4. Error Handling
- **400 Bad Request**: Returned when the request body is not a valid JSON.
- **422 Unprocessable Entity**: Returned when the input data is invalid or missing required fields.

5. Testing Strategy
- **Isolated Test Environment**: Used an in-memory SQLite database for testing.
- **Comprehensive Test Cases**: Covered all possible CRUD operations, edge cases, and error handling scenarios.

