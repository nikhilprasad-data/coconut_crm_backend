--sellers, locations
CREATE SCHEMA master;

--purchases, payments
CREATE SCHEMA finance; 

CREATE TABLE IF NOT EXISTS master.locations
	(
		address_id 	SERIAL,
		city      	VARCHAR(100)	NOT NULL,
		state 		VARCHAR(100)	NOT NULL,
		CONSTRAINT address_id_pk PRIMARY KEY(address_id)
	);

CREATE TABLE IF NOT EXISTS master.sellers
	(
		seller_id		SERIAL,
		seller_name 	VARCHAR(100)	NOT NULL,
		contact_number	VARCHAR(20)	NOT NULL,
		address_id	INT 			REFERENCES master.locations(address_id),
		is_active		BOOLEAN 		DEFAULT true
		CONSTRAINT seller_id_pk 	PRIMARY KEY (seller_id),
	);

CREATE TABLE IF NOT EXISTS finance.purchases
	(
		purchase_id		SERIAL,
		seller_id			INT			REFERENCES master.sellers(seller_id),
		purchase_date		DATE			NOT NULL,
		total_bags 		INT			NOT NULL,
		waste_pieces		INT			DEFAULT 0,
		rate_per_piece		DECIMAL(10,2)	NOT NULL,
--total_bill_amount ((total_bags * 30) - waste_piece) * rate_per_piece
		CONSTRAINT purchase_id_pk PRIMARY KEY(purchase_id) 
	);
	 
CREATE TABLE IF NOT EXISTS finance.payments
	(
		payment_id	SERIAL,
		seller_id		INT			REFERENCES master.sellers(seller_id),
		payment_date	DATE			NOT NULL,
		amount_paid	DECIMAL(12,2)	NOT NULL,
		payment_method	VARCHAR(50)	NOT NULL,
		CONSTRAINT payment_id_pk PRIMARY KEY(payment_id)
	);

CREATE TABLE IF NOT EXISTS master.users
(
	user_id 		SERIAL,
	username		VARCHAR(100)	UNIQUE NOT NULL,
	password_hash 	VARCHAR(255) 	NOT NULL,
	role 		VARCHAR(20) 	DEFAULT 	'seller',
	seller_id		INT 			REFERENCES master.sellers(seller_id),
	CONSTRAINT user_id_pk PRIMARY KEY(user_id)
);