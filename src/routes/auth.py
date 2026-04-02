from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from src.models.user import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/test', methods=['GET'])
def test_auth():
     try:

          return jsonify({
                         "status"  : "success",
                         "message" : "auth route is working perfectly"
          }), 200
      
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500

@auth_bp.route('/login/admin', methods= ['POST'])
def login_admin():
     try:
          data                = request.get_json()

          required_feilds     = ["username", "password"]

          for feild in required_feilds:

               if not data.get(feild) or not str(data.get(feild)).strip():
                    return jsonify({
                              "status"  : "error",
                              "message" : f"{feild}, is missing or empty. Please provide all the details"
                    }), 400


          username       = data.get("username").strip()
          password       = data.get("password").strip()

          existing_admin = User.query.filter_by(username= username, role= 'admin').first()

          if existing_admin and (check_password_hash(existing_admin.password_hash, password)) :

               access_token = create_access_token(identity= str(existing_admin.user_id))
               return jsonify({
                              "status"       : "success",
                              "message"      : f"sucessfully logged in as admin {username}",
                              "access_token" : access_token
               }), 200

          else:

               return jsonify({
                              "status"  : "error",
                              "message" : "Invalid username or password"
               }), 401
          
     except Exception as e:
          print(e)
          return jsonify({
                         "status" : "error",
                         "message" : "Internal server error"
          }), 500