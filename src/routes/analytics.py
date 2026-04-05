from flask import Blueprint, jsonify
from sqlalchemy import text
from src.db import db
from src.models.user import User
from src.models.seller import Seller
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.queries.analytics_queries import OUT_STANDING_BALANCE_QUERY,YEARLY_PURCHASE_QUERY,HIERARCHICAL_REVENUE_QUERY

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@analytics_bp.route('/balance/<int:seller_id>', methods= ['GET'])
@jwt_required()
def get_outstand_balance(seller_id):
     try:
          current_identity    = int(get_jwt_identity())
          current_user        = User.query.get(current_identity)

          if not current_user:
               return jsonify({
                              "status"  : "error",
                              "message" : "User not found"
               }), 404
          
          if current_user.role == 'Seller':
               if current_user.seller_id != seller_id:
                    return jsonify({
                                   "status"  : "error",
                                   "message" : "Access Denied. As seller you can't view other seller's outstanding balance"
                    }), 403
               
          existing_seller = Seller.query.get(seller_id)

          if not existing_seller:
               return jsonify({
                              "status"  : "error",
                              "message" : "Seller not found"
               }), 404

          result = db.session.execute(text(OUT_STANDING_BALANCE_QUERY), {"target_id" : seller_id}).mappings().fetchone()

          return jsonify({
                         "status"  : "success",
                         "result"  : dict(result)
          }), 200
     
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  :    "error",
                         "message" :    "Internal Server error"
          }), 500

@analytics_bp.route('/yearly-purchase', methods= ['GET'])
@jwt_required()
def get_yearly_purchase_report():
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
                              "message" : "Access Denied. As seller you can't access reports"
               }), 403
          
          result = db.session.execute(text(YEARLY_PURCHASE_QUERY)).mappings().fetchall()

          report_data = [ dict(row) for row in result]

          return jsonify({
                         "status"  : "success",
                         "report"  : report_data
          }), 200
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal server error"
          }), 500

@analytics_bp.route('/revenue-hierarchy', methods= ['GET'])
@jwt_required()
def get_revenue_hierarchy():
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
                              "message" : "Access Denied. As seller you can't see the reports"
               }), 403
          
          result = db.session.execute(text(HIERARCHICAL_REVENUE_QUERY)).mappings().fetchall()

          hierarchical_report = [dict(raw) for raw in result]

          return jsonify({
                         "status"                 : "success",
                         "hierarchical_report"    : hierarchical_report
          })
     except Exception as e:
          print(e)
          return jsonify({
                         "status"  : "error",
                         "message" : "Internal Server error" 
          }), 500