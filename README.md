# 🥥 Coconut CRM - B2B Wholesale Management Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

> **Live Backend API (Render):** https://coconut-crm-api.onrender.com

> **Live Frontend (Vercel):** https://coconut-crm-frontend.vercel.app

> **API Documentation (Postman):** https://documenter.getpostman.com/view/53629100/2sBXqGrMnT

## 📖 Overview (The Problem it Solves)
Coconut CRM is a robust, production-ready backend designed to transition traditional wholesale businesses from a manual, paper-based ecosystem to a fully digitized platform. It features a structured, normalized PostgreSQL database model to track complex multi-party payments, purchase orders, and generate automated daily business reporting. 

## ✨ Core Features
1. **Role-Based Access Control (RBAC):** Secure JWT authentication to distinguish workflows between `Admin` and `Seller` roles.
2. **Automated SQL Analytics:** Complex data extraction and reporting (Geographic Revenue & Territory Analytics, Outstanding Balances, Regional Leaderboards, Financial Reports & Revenue Analytics) using SQL CTEs, PIVOT, and Window Functions.
3. **Scalable Database Architecture:** A highly normalized schema designed to prevent data redundancy and handle thousands of transactions seamlessly.
4. **Data Flow Testing:** Custom data seeding (`generate_seed.py`) to accurately simulate API endpoint traffic and validate query performance.

## 💻 Tech Stack
* **Backend Framework:** Python, Flask
* **Database:** PostgreSQL
* **Security:** JSON Web Tokens (JWT), Password Hashing
* **Environment Management:** `python-dotenv`

## 🗄️ Database Architecture
The database follows a normalized relational structure:
* **`master.users`**: Manages secure system access, credentials, and RBAC mapping (Admin/Seller mapping).
* **`master.locations`**: Tracks regional data (City, State).
* **`master.sellers`**: Manages seller business profiles and contact details.
* **`finance.purchases`**: Logs inventory intake (Bags, Waste pieces, Rate).
* **`finance.payments`**: Tracks multi-party transactions and payment methods.

Follow these steps to run the backend environment locally on your machine:

**1. Clone the repository**
> ```bash
> git clone [https://github.com/nikhilprasad-data/coconut_crm_backend.git](https://github.com/nikhilprasad-data/coconut_crm_backend.git)
> cd coconut_crm_backend
> ```

**2. Create and activate a virtual environment**
> ```bash
> # Windows
> python -m venv venv
> venv\Scripts\activate
> 
> # Mac/Linux
> python3 -m venv venv
> source venv/bin/activate
> ```

**3. Install dependencies**
> ```bash
> pip install -r requirements.txt
> ```

**4. Environment Variables setup**
Create a `.env` file in the root directory and add your credentials:
> ```env
> DATABASE_URL=postgresql://user:password@localhost:5432/coconut_crm
> JWT_SECRET_KEY=your_super_secret_key
> ```

**5. Database Initialization (Strict Order)**
Execute the SQL scripts in your PostgreSQL instance in this specific order:
* Run `database/schema.sql` (Creates tables)
* Run `database/seed.sql` or use `database/generate_seed.py` (Injects testing data)
* Run `database/queries.sql` (For reporting and analytics)

**6. Start the Application**
`run.py` is the entry point of our backend architecture.
> ```bash
> python run.py
> ```

## 📡 API Endpoints (Quick Reference)

Detailed documentation is available in the Postman collection linked at the top.

* `POST /api/auth/login` - Authenticate users and issue JWT.
* `GET /api/dashboard/summary` - Fetch automated business reports (Admin only).
* `POST /api/finance/purchases` - Log a new wholesale purchase.
* `GET /api/finance/outstanding` - Calculate net outstanding balances.

---
*Built with passion and pure engineering honesty by [Nikhil Prasad](https://github.com/nikhilprasad-data).*