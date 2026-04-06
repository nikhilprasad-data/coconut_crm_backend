from flask import Blueprint, jsonify, request
from src.models.seller import Seller
from src.models.user import User
from src.models.location import Location
from src.db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

seller_bp = Blueprint('seller', __name__, url_prefix='/api/seller')

@seller_bp.route('/add', methods= ['POST'])
@jwt_required()
def add_seller():
     try:
          current_identity    = int(get_jwt_identity())
          current_user        = User.query.get(current_identity) 

          if not current_user :
               return jsonify({
                              "status"  : "error",
                              "message" : "User not found"
               }), 404
          
          if current_user.role == 'Seller':
               return jsonify({
                              "status"  : "error",
                              "message" : "Access Denied. As seller you can't delete any seller"
               }), 403

          data                =    request.get_json()

          required_fields     =    ["city", "state", "seller_name", "contact_number", "username", "password"]

          for feild in required_fields:

               if not (data.get(feild)) or not (str(data.get(feild)).strip()):

                    return jsonify({
                              "status"  : "error",
                              "message" : f"{feild}, is missing or empty. Please provide all the details"
                    }), 400
               
          city                =    data.get("city").strip().title()
          state               =    data.get("state").strip().title()

          seller_name         =    data.get("seller_name").strip().title()
          contact_number      =    data.get("contact_number").strip()

          user_name           =    data.get("username").strip()
          password_hash       =    generate_password_hash(data.get("password").strip())

          existing_seller     =    Seller.query.filter_by(seller_name= seller_name,contact_number= contact_number).first()

          if existing_seller:
               return jsonify({
                              "status"  : "error",
                              "message" : "Seller already exists"
               }), 409
   
          existing_location = Location.query.filter_by(city= city, state= state).first()

          if existing_location:

               final_address_id = existing_location.address_id

          else:

               new_location = Location(city= city, state= state)
               db.session.add(new_location)
               db.session.flush()
               final_address_id = new_location.address_id

          new_seller = Seller(seller_name= seller_name, contact_number= contact_number, address_id= final_address_id)
          db.session.add(new_seller)
          db.session.flush()

          new_user = User(username= user_name, password_hash= password_hash,role= 'Seller', seller_id= new_seller.seller_id)
          db.session.add(new_user)
          db.session.commit()
     
          return jsonify({
                         "status"  : "success",
                         "message" : f"{seller_name}, added successfully"
          }),201
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500

@seller_bp.route('/data', methods= ['GET'])
@jwt_required()
def get_sellers():
     try:

          current_identity    = int(get_jwt_identity())
          current_user        = User.query.get(current_identity) 

          if not current_user :
               return jsonify({
                              "status"  : "error",
                              "message" : "User not found"
               }), 404
          
          if current_user.role == 'Seller':
               return jsonify({
                              "status"  : "error",
                              "message" : "Access Denied. As seller you can't delete any seller"
               }), 403
          
          all_seller = Seller.query.filter_by(is_active= True).all()

          if not all_seller:
               return jsonify({
                              "status"  : "error",
                              "message" : "No seller found"
               }), 404
          
          seller_list = []

          for seller in all_seller:

               loc            = Location.query.filter_by(address_id = seller.address_id).first()

               seller_dict    ={  
                                   "seller_id"      : seller.seller_id, 
                                   "seller_name"    : seller.seller_name, 
                                   "contact_number" : seller.contact_number,
                                   "city"           : loc.city,
                                   "state"          : loc.state
                              }
               
               seller_list.append(seller_dict)

          return jsonify({
                              "status" : "success",
                              "data"   : seller_list
               }), 200

     except Exception as e:
          print(e)
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500

@seller_bp.route('delete/<int:seller_id>', methods= ['DELETE'])
@jwt_required()
def delete_seller(seller_id):
     try:
          current_identity    = int(get_jwt_identity())
          current_user        = User.query.get(current_identity) 

          if not current_user :
               return jsonify({
                              "status"  : "error",
                              "message" : "User not found"
               }), 404
          
          if current_user.role == 'Seller':
               return jsonify({
                              "status"  : "error",
                              "message" : "Access Denied. As seller you can't delete any seller"
               }), 403
          
          seller = Seller.query.get(seller_id)

          if not seller:
               return jsonify({
                              "status"  : "error",
                              "message" : f"{seller_id}, seller id not found"
               }), 404
          
          seller.is_active = False
          db.session.commit()
          return jsonify({
                         "status"  : "success",
                         "message" : "Seller deleted successfully"
          }), 200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500