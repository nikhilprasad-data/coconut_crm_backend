from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required,get_jwt_identity
from src.models.seller import Seller
from src.models.purchase import Purchase
from src.models.user import User
from src.db import db

purchase_bp = Blueprint('purchase', __name__, url_prefix='/api/purchase')

@purchase_bp.route('/all', methods= ['GET'])
@jwt_required()
def all_get_purchase():
     try:
          current_identity    = int(get_jwt_identity())
          current_user        = User.query.get(current_identity)

          if not current_user:
               return jsonify({
                              "status"  : "error",
                              "message" : "User not found"
               }), 404
          
          if current_user.role != 'admin':
               return jsonify({
                              "status"  : "error",
                              "message" : "Access denied. Only Admin can view all purchase records"
               }), 403
          
          all_purchase        = Purchase.query.all()
          all_purchase_list    = []
          for purchase in all_purchase:
               purchase_dict = {
                              "purchase_id"       : purchase.purchase_id,
                              "purchase_date"     : str(purchase.purchase_date),
                              "total_bags"        : purchase.total_bags,
                              "waste_pieces"      : purchase.waste_pieces,
                              "rate_per_piece"    : float(purchase.rate_per_piece),
                              "total_amount"      : round(float(((purchase.total_bags * 30) - purchase.waste_pieces)*purchase.rate_per_piece),2)}
               
               all_purchase_list.append(purchase_dict)

          return jsonify({
                         "status"  : "success",
                         "data"    : all_purchase_list
          }), 200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500

@purchase_bp.route('/data/<int:seller_id>', methods= ['GET'])
@jwt_required()
def get_purchase(seller_id):
     try:
          current_user_identity = get_jwt_identity()
          current_user          = User.query.filter_by(user_id= int(current_user_identity)).first()

          if not current_user:
               return jsonify({
                              "status" : "error",
                              "message": "User not forund"
               }), 404
          
          if current_user.role == 'Seller':
               if current_user.seller_id != seller_id:
                    return jsonify({
                              "status" : "error",
                              "message": "Access Denied. You can't see other seller's purchase."
                    }), 403
                    
          existing_seller     = Seller.query.get(seller_id)
          if not existing_seller:
               return jsonify({
                              "status" : "error",
                              "message": f"Seller id {seller_id}, not exists"
               }), 404
          
          seller_dict  = {
                              "seller_id"              : existing_seller.seller_id,
                              "seller_name"            : existing_seller.seller_name,
                              "seller_contact_number"  : existing_seller.contact_number}

          all_purchase = Purchase.query.filter_by(seller_id= seller_id).all()

          purchase_list = []

          for purchase in all_purchase:
               purchase_dict = {
                                   "purchase_id"       : purchase.purchase_id,
                                   "purchase_date"     : str(purchase.purchase_date),
                                   "total_bags"        : purchase.total_bags,
                                   "waste_pieces"      : purchase.waste_pieces,
                                   "rate_per_piece"    : float(purchase.rate_per_piece),
                                   "total_amount"      : round(float(((purchase.total_bags * 30) - purchase.waste_pieces)*purchase.rate_per_piece),2)}
               
               purchase_list.append(purchase_dict)

          return jsonify({
                         "status"       : "success",
                         "seller_data"  : seller_dict,
                         "purchase_data": purchase_list
          }), 200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500

@purchase_bp.route('/add', methods= ['POST'])
@jwt_required()
def add_purchase():
     try:
          current_identity    = int(get_jwt_identity())
          current_user        = User.query.get(current_identity)

          if not current_user:
               return jsonify({
                              "status"  : "error",
                              "message" : "User not found"
               }), 404
          
          if current_user.role == 'Seller':
               return jsonify({
                              "status"  : "error",
                              "message" : "Access Denied. As a seller you can't add purchase."
               }), 403
          
          data  = request.get_json()

          required_fields = ["seller_id", "purchase_date", "total_bags", "waste_pieces", "rate_per_piece"]

          for field in required_fields:

               if field not in data or data[field] is None:
                    return jsonify({
                                   "status"  : "error",
                                   "message" : f"{field} is missing or empty. Please provide all the details"
                    }), 400
          try:
               seller_id = int(data["seller_id"])

          except Exception as e:
               print(e)
               return jsonify({
                              "status"  : "error",
                              "message" : f"Please input required seller_id in correct data type format"
               }), 400
          
          existing_seller = Seller.query.get(seller_id)

          if not existing_seller:
               return jsonify({
                              "status"  : "error",
                              "message" : "Seller not found"
               }), 404
          
          try:
               purchase_date  = str((data)["purchase_date"])
               total_bags     = int((data)["total_bags"])
               waste_pieces   = int((data)["waste_pieces"])
               rate_per_piece = float((data)["rate_per_piece"])
          
          except Exception as e:
               print(e)
               return jsonify({
                              "status"  : "error",
                              "message" : "Please input required fields in correct data type format"
               }), 400
          
          new_purchase = Purchase(seller_id= seller_id, purchase_date= purchase_date, total_bags= total_bags, waste_pieces= waste_pieces, rate_per_piece= rate_per_piece)
          db.session.add(new_purchase)
          db.session.commit()
          return jsonify({
                         "status"  : "success",
                         "message" : f"Successfully added purchase on seller id {seller_id}"
               }), 200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500

@purchase_bp.route('/update/<int:purchase_id>', methods= ['PATCH'])
@jwt_required()
def update_purchase(purchase_id):
     try:
          current_identity = int(get_jwt_identity())
          current_user     = User.query.get(current_identity)

          if not current_user:
               return jsonify({
                              "status"  :  "error",
                              "message" : "User not found"
               }), 404
        
          if current_user.role == 'Seller':
               return jsonify({
                              "status"  : "error",
                              "message" : "Access Denied. Seller can't update any purchase"
               }), 403
        
          existing_purchase = Purchase.query.get(purchase_id)

          if not existing_purchase:
             return jsonify({
                              "status"  : "error",
                              "message" : f"Purchase id {purchase_id}, not found"
             }), 404
        
          data = request.get_json()
          updated_fields = []

          if "seller_id" in data:
               try:
                    seller_id = int(data.get("seller_id")) 
                    existing_seller = Seller.query.get(seller_id)

                    if not existing_seller:
                         return jsonify({
                                        "status"  : "error",
                                        "message" : "Seller not found"
                         }), 404
                         
                    existing_purchase.seller_id   = seller_id
                    updated_fields.append({"seller_id": seller_id})

               except Exception as e:
                    print(e)
                    return jsonify({
                              "status"  : "error",
                              "message" : "Wrong data type for seller_id"
                    }), 400
          
          if "purchase_date" in data:
               try:
                    purchase_date                      = str(data.get("purchase_date"))
                    existing_purchase.purchase_date    = purchase_date

                    updated_fields.append({"purchase_date" : purchase_date})

               except Exception as e:
                    print(e)
                    return jsonify({
                              "status"  : "error",
                              "message" : "Wrong data type for purchase_date"
                    }), 400
          
          if "total_bags" in data:
               try:
                    total_bags                    = int(data.get("total_bags"))
                    existing_purchase.total_bags  = total_bags

                    updated_fields.append({"total_bags" : total_bags})

               except Exception as e:
                    print(e)
                    return jsonify({
                              "status"  : "error",
                              "message" : "Wrong data type for total_bags"
                    }), 400
               
          if "waste_pieces" in data:
               try:
                    waste_pieces                       = int(data.get("waste_pieces"))
                    existing_purchase.waste_pieces     = waste_pieces

                    updated_fields.append({"waste_pieces" : waste_pieces})

               except Exception as e:
                    print(e)
                    return jsonify({
                              "status"  : "error",
                              "message" : "Wrong data type for waste_pieces"
                    }), 400
          
          if "rate_per_piece" in data:
               try:
                    rate_per_piece                     = float(data.get("rate_per_piece"))
                    existing_purchase.rate_per_piece   = rate_per_piece

                    updated_fields.append({"rate_per_piece" : rate_per_piece})

               except Exception as e:
                    print(e)
                    return jsonify({
                              "status"  : "error",
                              "message" : "Wrong data type for rate_per_piece"
                    }), 400
          
          if len(updated_fields) == 0:
               return jsonify({
                              "status"  : "error",
                              "message" : "No valid fields provided for update"
               }), 400
          
          db.session.commit()
          return jsonify({
                         "status"            : "success",
                         "message"           : f"Purchase id {purchase_id} updated successfully",
                         "fields_updated"    : updated_fields
          }), 200
          
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500

@purchase_bp.route('/replace/<int:purchase_id>', methods= ['PUT'])
@jwt_required()
def replace_purchase(purchase_id):
     try:
          current_identity    = int(get_jwt_identity())
          current_user        = User.query.get(current_identity)

          if not current_user:
               return jsonify({
                              "status"  : "error",
                              "message" : "User not found"
               }), 404
          
          if current_user.role == 'Seller':
               return jsonify({
                              "status"  : "error",
                              "message" : "Access Denied. Seller can't replace purchase data"
               }), 403
          
          existing_purchase = Purchase.query.get(purchase_id)

          if not existing_purchase:
               return jsonify({
                              "status"  : "error",
                              "message" : f"Purchase id {purchase_id} not found"
               }), 404
          
          data = request.get_json()

          required_fields = ["seller_id", "purchase_date", "total_bags", "waste_pieces", "rate_per_piece"]

          for field in required_fields:

               if field not in data or data[field] is None:
                    return jsonify({
                                   "status"  : "error",
                                   "message" : f"{field} is missing or empty. Please provide all the details"
                    }), 400
               
          replaced_data = []
          try:
               seller_id = int(data.get("seller_id"))
               existing_seller = Seller.query.get(seller_id)
               replaced_data.append({"seller_id" : seller_id})

               if not existing_seller:
                    return jsonify({
                                   "status"  : "error",
                                   "message" : "Seller not found"
                    }), 404
               
          except Exception as e:
               print(e)
               return jsonify({
                              "status"  : "error",
                              "message" : "Wrong data type for seller_id"
               }), 400
          
          try:
               purchase_date = str(data.get("purchase_date"))
               replaced_data.append({"purchase_date" : purchase_date})

               total_bags = float(data.get("total_bags"))
               replaced_data.append({"total_bags" : total_bags})

               waste_pieces = int(data.get("waste_pieces"))
               replaced_data.append({"waste_pieces" : waste_pieces})

               rate_per_piece = float(data.get("rate_per_piece"))
               replaced_data.append({"rate_per_piece" : rate_per_piece})

          except Exception as e:
               print(e)
               return jsonify({
                              "status"  : "error",
                              "message" : "Please input required fields in correct data type format"
               }), 400
          
          existing_purchase.seller_id        = seller_id
          existing_purchase.purchase_date    = purchase_date
          existing_purchase.total_bags       = total_bags
          existing_purchase.waste_pieces     = waste_pieces
          existing_purchase.rate_per_piece   = rate_per_piece

          db.session.commit()

          return jsonify({
                         "status"            : "success",
                         "message"           : f"Purchase {purchase_id}, replaced successfully",
                         "replaced_data"     : replaced_data

          }), 200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"            : "error",
                         "message"           : "Internal server error"
          }), 500 

@purchase_bp.route('/my-purchase',methods= ['GET'])
@jwt_required()
def my_purchase():
     try:
          current_identity    = int(get_jwt_identity())
          current_user        = User.query.get(current_identity)

          if not current_user:
               return jsonify({
                    "status"  : "error",
                    "message" : "User not found"
               }), 404

          if current_user.role != "Seller":
               return jsonify({
                              "status"  : "error",
                              "message" : "Access denied. Only Sellers can view their own purchase records"
               }), 403
          
          purchase_list = []
          existing_purchase = Purchase.query.filter_by(seller_id= current_user.seller_id).all()
          for purchase in existing_purchase:
               purchase_dict = {
                              "purchase_id"       : purchase.purchase_id,
                              "purchase_date"     : str(purchase.purchase_date),
                              "total_bags"        : purchase.total_bags,
                              "waste_pieces"      : purchase.waste_pieces,
                              "rate_per_piece"    : float(purchase.rate_per_piece),
                              "total_amount"      : round(float(((purchase.total_bags * 30) - purchase.waste_pieces)*purchase.rate_per_piece),2)}
               purchase_list.append(purchase_dict)

          return jsonify({
                         "status"  : "success",
                         "data"    : purchase_list
          }), 200

     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500