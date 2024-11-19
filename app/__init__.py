from flask import Flask
from .database import init_db
from .database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'
    #save some memory
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #initialize db
    db.init_app(app)
    print("db object:", db)

    with app.app_context():
        from .routes import bp
        app.register_blueprint(bp)

    return app
