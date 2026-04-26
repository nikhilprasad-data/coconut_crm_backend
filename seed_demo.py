from src.db import db
from src import create_app
from src.models.user import User
from src.models.location import Location
from src.models.seller import Seller 
from src.models.payment import Payment
from src.models.purchase import Purchase
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
     db.create_all()

     try:

          demo_admin_username = "demo_admin_11"
          demo_admin_password = "demo_password"

          existing_demo_admin = User.query.filter_by(username= demo_admin_username, role= "admin").first()

          if existing_demo_admin:
               print("Demo Admin already exists.")

          else:
               demo_amdin = User(username= demo_admin_username, password_hash= generate_password_hash(demo_admin_password), role= "admin")
               db.session.add(demo_amdin)
               db.session.commit()
               print("Demo Admin created successfully.")
          
          demo_seller_username = "demo_seller_12"
          demo_seller_password = "demo_password"

          demo_seller_city    = "Kuttiyadi"
          demo_seller_state   = "Kerala"

          demo_seller_name              = "Guest Wholesale"
          demo_seller_contact_number    = "+91 8620901229"

          existing_demo_seller  = User.query.filter_by(username= demo_seller_username, role= "Seller").first()

          if existing_demo_seller:
               print("Demo Seller already exists.")
          
          else:
               existing_location = Location.query.filter_by(city= demo_seller_city, state= demo_seller_state).first()
               if existing_location:
                    final_address_id = existing_location.address_id
               
               else:
                    new_location = Location(city= demo_seller_city, state= demo_seller_state)
                    db.session.add(new_location)
                    db.session.flush()
                    final_address_id = new_location.address_id

               demo_seller_add = Seller(seller_name= demo_seller_name, contact_number= demo_seller_contact_number, address_id= final_address_id)               
               db.session.add(demo_seller_add)
               db.session.flush()

               demo_seller = User(username= demo_seller_username, password_hash= generate_password_hash(demo_seller_password), role= "Seller", seller_id= demo_seller_add.seller_id)
               db.session.add(demo_seller)
               db.session.flush()

               print("Demo Seller created successfully.")

               sid = demo_seller_add.seller_id 

               pur_data = [
                    Purchase(seller_id=sid, purchase_date="2024-05-12", total_bags=40, waste_pieces=2, rate_per_piece=45.50),
                    Purchase(seller_id=sid, purchase_date="2024-11-28", total_bags=35, waste_pieces=5, rate_per_piece=42.00),
                    
                    Purchase(seller_id=sid, purchase_date="2025-02-15", total_bags=50, waste_pieces=1, rate_per_piece=48.25),
                    Purchase(seller_id=sid, purchase_date="2025-06-20", total_bags=28, waste_pieces=4, rate_per_piece=39.90),
                    Purchase(seller_id=sid, purchase_date="2025-09-10", total_bags=45, waste_pieces=2, rate_per_piece=46.00),
                    Purchase(seller_id=sid, purchase_date="2025-12-05", total_bags=60, waste_pieces=8, rate_per_piece=41.50),
                    
                    Purchase(seller_id=sid, purchase_date="2026-01-18", total_bags=32, waste_pieces=0, rate_per_piece=50.00),
                    Purchase(seller_id=sid, purchase_date="2026-03-22", total_bags=48, waste_pieces=3, rate_per_piece=47.75),
                    Purchase(seller_id=sid, purchase_date="2026-04-10", total_bags=25, waste_pieces=1, rate_per_piece=49.00)
               ]
               

               pay_data = [
                    Payment(seller_id=sid, payment_date="2024-06-01", amount_paid=45000.00, payment_method="Bank Transfer"),
                    Payment(seller_id=sid, payment_date="2024-12-10", amount_paid=30000.00, payment_method="UPI"),
                    
                    Payment(seller_id=sid, payment_date="2025-03-01", amount_paid=60000.00, payment_method="Cheque"),
                    Payment(seller_id=sid, payment_date="2025-07-05", amount_paid=25000.00, payment_method="Cash"),
                    Payment(seller_id=sid, payment_date="2025-10-01", amount_paid=50000.00, payment_method="Bank Transfer"),
                    
                    Payment(seller_id=sid, payment_date="2026-02-05", amount_paid=40000.00, payment_method="UPI"),
                    Payment(seller_id=sid, payment_date="2026-04-05", amount_paid=55000.00, payment_method="Cheque")
               ]

               db.session.add_all(pur_data)
               db.session.add_all(pay_data)
               
               db.session.commit() 
               
               print("Demo Seller and HEAVY Data injected successfully!")

     except Exception as e:
          print(e)