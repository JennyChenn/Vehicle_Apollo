from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    #integrate db with flask 
    db.init_app(app)
    # app's context
    with app.app_context():
        #creates all tables defined by the models
        db.create_all()
