from flask import Blueprint, jsonify,request
from flask_jwt_extended import get_jwt_identity,jwt_required
from src.models.payment import Payment
from src.models.seller import Seller
from src.models.user import User
from src.db import db

payment_bp = Blueprint('payment', __name__, url_prefix='/api/payment')

@payment_bp.route('/all', methods= ['GET'])
@jwt_required()
def all_get_payment():
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
                              "message" : "Access denied. Only Admin can view all payment records"
               }), 403
          
          all_payment         = Payment.query.all()
          all_payment_list    = []
          for payment in all_payment:
               payment_dict = {
                              "payment_id"        : payment.payment_id,
                              "seller_id"         : payment.seller_id,
                              "payment_date"      : str(payment.payment_date),
                              "amount_paid"       : round(float(payment.amount_paid),2),
                              "payment_method"    : payment.payment_method}
               
               all_payment_list.append(payment_dict)
          
          return jsonify({
                         "status"  : "success",
                         "data"    : all_payment_list
          }), 200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500

@payment_bp.route('/data/<int:seller_id>',methods=['GET'])
@jwt_required()
def get_payment(seller_id):
     try:
          current_identity = int(get_jwt_identity())
          current_user = User.query.filter_by(user_id= current_identity).first()

          if not current_user:
               return jsonify({
                              "status"  : "error",
                              "message" : "User not found"
               }), 404
          
          if current_user.role == 'Seller':
               if current_user.seller_id != seller_id:
                    return jsonify({
                                   "status" : "error",
                                   "message" : "Access Denied. You can't see other seller's payments"
                    }), 403
          
          existing_seller = Seller.query.get(seller_id)

          if not existing_seller:
               return jsonify({
                              "status" : "error",
                              "message" : f"Seller id {seller_id}, not exists"
                    }), 404
          
          seller_dict = {
                         "seller_id"              : existing_seller.seller_id,
                         "seller_name"            : existing_seller.seller_name,
                         "seller_contact_number"  : existing_seller.contact_number
          }
          payment_list = []

          all_payment = Payment.query.filter_by(seller_id= existing_seller.seller_id).all()

          for payment in all_payment:

               payment_dict = {
                              "payment_id"        : payment.payment_id,
                              "seller_id"         : payment.seller_id,
                              "payment_date"      : str(payment.payment_date),
                              "amount_paid"       : round(float(payment.amount_paid),2),
                              "payment_method"    : payment.payment_method}
               
               payment_list.append(payment_dict)

          return jsonify({
                         "status"       : "success",
                         "seller_data"  : seller_dict,
                         "payment"      : payment_list
          }),200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500
     
@payment_bp.route('/add', methods= ['POST'])
@jwt_required()
def add_payment():
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
                              "message" : "Access Denied. As seller you can't add payment" 
               }), 403
          
          data = request.get_json()

          required_fields = ["seller_id", "payment_date", "amount_paid", "payment_method"]

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
                              "message" : "Please input required seller_id in correct data type format"
               }), 400
          
          existing_seller = Seller.query.get(seller_id)

          if not existing_seller:
               return jsonify({
                              "status" : "error",
                              "message" : "Seller not found"
               }), 404

          try:
               payment_date   = str(data["payment_date"])
               amount_paid    = float(data["amount_paid"])
               payment_method = str(data["payment_method"]).strip().title()

          except Exception as e:
               print(e)
               return jsonify({
                              "status"  : "error",
                              "message" : "Please input required fields in correct data type format"
               }), 400
          
          new_payment = Payment(seller_id= seller_id, payment_date= payment_date, amount_paid= amount_paid, payment_method= payment_method)
          db.session.add(new_payment)
          db.session.commit()
          return jsonify({
                         "status"  : "success",
                         "message" : f"Successfully added payment on seller id {seller_id}"
               }), 200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500

@payment_bp.route('/update/<int:payment_id>', methods= ['PATCH'])
@jwt_required()
def update_payment(payment_id):
     try:
          current_identity    = int(get_jwt_identity())
          current_user        = User.query.get(current_identity)

          if not current_user:
               return jsonify({
                              "status"  : "success",
                              "message" : "User not found"
               }), 404
          
          if current_user.role == 'Seller':
               return jsonify({
                              "status"  :"error",
                              "message" : "Access Denied. As seller you can't update payment" 
               }), 403
          
          existing_payment = Payment.query.get(payment_id)

          if not existing_payment:
               return jsonify({
                              "status"  : "error",
                              "message" : "Payment not found"
               }), 404
          
          data = request.get_json()          
          updated_feilds = []

          if "seller_id" in data:
               try:
                    seller_id = int(data.get("seller_id"))
                    existing_seller = Seller.query.get(seller_id)

                    if not existing_seller:
                         return jsonify({
                                        "status" : "error",
                                        "message": "Seller not found"
                         }), 404
                    
                    existing_payment.seller_id = seller_id
                    updated_feilds.append({"seller_id" : seller_id})

               except Exception as e:
                    print(e)
                    return jsonify({
                                   "status"  : "error",
                                   "message" : "Wrong data type for seller_id"
                    }), 400
               
          if "payment_date" in data:
               try:
                    payment_date = str(data.get("payment_date"))
                    
                    existing_payment.payment_date = payment_date
                    updated_feilds.append({"payment_date" : payment_date})

               except Exception as e:
                    print(e)
                    return jsonify({
                                   "status"  : "error",
                                   "message" : "Wrong data type for payment_date"
                    }), 400
          
          if "amount_paid" in data:
               try:
                    amount_paid = float(data.get("amount_paid"))
                    
                    existing_payment.amount_paid = amount_paid
                    updated_feilds.append({"amount_paid" : amount_paid})

               except Exception as e:
                    print(e)
                    return jsonify({
                                   "status"  : "error",
                                   "message" : "Wrong data type for amount_paid"
                    }), 400
          
          if "payment_method" in data:
               try:
                    payment_method = str(data.get("payment_method")).strip().title()
                    
                    existing_payment.payment_method = payment_method
                    updated_feilds.append({"payment_method" : payment_method})

               except Exception as e:
                    print(e)
                    return jsonify({
                                   "status"  : "error",
                                   "message" : "Wrong data type for payment_method"
                    }), 400
          if len(updated_feilds) == 0:
               return jsonify({
                              "status"  : "error",
                              "message" : "No valid fields provided for update"
               }), 400
               
          db.session.commit()
          return jsonify({
                         "status"            : "success",
                         "message"           : f"Payment id {payment_id}, updated successfully",
                         "field_updated"     : updated_feilds
          }), 200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500 
     
@payment_bp.route('/replace/<int:payment_id>', methods= ['PUT'])
@jwt_required()
def replace_payment(payment_id):
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
                              "message" : "Access Denied. As seller you can't replace payment"
               }), 403
          
          existing_payment = Payment.query.get(payment_id)

          if not existing_payment:
               return jsonify({
                              "status"  : "error",
                              "message" : f"Payment id {payment_id}, not found"
               }), 404
          
          data = request.get_json()

          required_fields = ["seller_id", "payment_date", "amount_paid", "payment_method"]

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
               payment_date = str(data.get("payment_date"))
               replaced_data.append({"payment_date" : payment_date})

               amount_paid = float(data.get("amount_paid"))
               replaced_data.append({"amount_paid" : amount_paid})

               payment_method = str(data.get("payment_method")).strip().title()
               replaced_data.append({"payment_method" : payment_method})
          
          except Exception as e:
               print(e)
               return jsonify({
                              "status"  : "error",
                              "message" : "Please input required fields in correct data type format"
               }), 400
          
          existing_payment.seller_id         = seller_id
          existing_payment.payment_date      = payment_date
          existing_payment.amount_paid       = amount_paid
          existing_payment.payment_method    = payment_method

          db.session.commit()

          return jsonify({
                         "status"            : "success",
                         "message"           : f"Payment {payment_id}, replaced successfully",
                         "replaced_data"     : replaced_data

          }), 200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"            : "error",
                         "message"           : "Internal server error"
          }), 500 

@payment_bp.route('/my-payment',methods= ['GET'])
@jwt_required()
def my_payment():
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
                              "message" : "Access denied. Only Sellers can view their own payment records"
               }), 403
          
          payment_list = []
          existing_payment = Payment.query.filter_by(seller_id= current_user.seller_id).all()
          for payment in existing_payment:
               payment_dict = {
                              "payment_id"        : payment.payment_id,
                              "payment_date"      : str(payment.payment_date),
                              "amount_paid"       : round(float(payment.amount_paid),2),
                              "payment_method"    : payment.payment_method}
               payment_list.append(payment_dict)
                    
          return jsonify({
                         "status"  : "success",
                         "data"    : payment_list
          }), 200

     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500