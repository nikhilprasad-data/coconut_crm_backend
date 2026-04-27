from flask import Flask
from .db import db
from .config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
     app=Flask(__name__)

     CORS(app, resources= {
          r"/*" : {
               "origins" : [
                    "https://coconut-crm-frontend.vercel.app",
                    "http://localhost:3000"
               ]
          }
     }, supports_credentials= True)

     app.config.from_object(Config)

     db.init_app(app)

     jwt = JWTManager(app)

     from .routes.auth import auth_bp
     app.register_blueprint(auth_bp)

     from .routes.seller import seller_bp
     app.register_blueprint(seller_bp)

     from .routes.purchase import purchase_bp
     app.register_blueprint(purchase_bp)

     from .routes.payment import payment_bp
     app.register_blueprint(payment_bp)

     from .routes.analytics import analytics_bp
     app.register_blueprint(analytics_bp)

     return app