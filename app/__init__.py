from flask import Flask
from flask_cors import CORS
from app.extensions import Base, engine
from app.routes.motivation_routes import motivation_bp
from app.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    
    # enable cros
    CORS(app)

    # create tables
    Base.metadata.create_all(bind=engine)

    # register blueprint
    app.register_blueprint(motivation_bp)
    app.register_blueprint(auth_bp)

    return app
