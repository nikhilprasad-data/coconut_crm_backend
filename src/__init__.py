from flask import Flask
from .db import db
from .config import Config
from flask_jwt_extended import JWTManager

def create_app():
     app=Flask(__name__)

     app.config.from_object(Config)

     db.init_app(app)

     jwt = JWTManager(app)

     from .routes.auth import auth_bp
     app.register_blueprint(auth_bp)

     from .routes.seller import seller_bp
     app.register_blueprint(seller_bp)

     return app