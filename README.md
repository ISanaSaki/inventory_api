# 📦 Inventory Management System API

A production-ready **Inventory Management System** built with **FastAPI**,  
**PostgreSQL**, and **SQLAlchemy**, featuring secure JWT authentication,  
role-based access control, inventory tracking, reporting, and Docker support.

This project is designed with modular architecture, clean service-layer separation, and strong business rule enforcement suitable for real-world backend systems.

---

## 🚀 Features

- ✨ JWT Authentication (Access & Refresh Tokens)
- ✨ Role-based access control (Admin / Staff)
- ✨ Secure password hashing (Argon2)
- ✨ Product & category management
- ✨ Supplier management
- ✨ Inventory stock-in / stock-out operations
- ✨ Stock validation (prevents negative inventory)
- ✨ Unique SKU enforcement
- ✨ Low-stock monitoring
- ✨ Inventory reports & analytics
- ✨ Login & security audit logging
- ✨ PostgreSQL with Alembic migrations
- ✨ Dockerized deployment

---

## 🛠 Tech Stack

- **Backend:** FastAPI  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy  
- **Authentication:** JWT (Access & Refresh Tokens)  
- **Security:** Argon2 password hashing  
- **Migrations:** Alembic  
- **Containerization:** Docker & Docker Compose  

---

## 📂 Project Structure

```txt

app/
├── auth/          # Authentication & token management
├── users/         # User and role management
├── products/      # Product management
├── categories/    # Category management
├── inventory/     # Stock transactions (in/out)
├── suppliers/     # Supplier management
├── reports/       # Reporting & analytics
├── audit/         # Login & security audit logs
├── core/          # Configuration & security settings
├── db/            # Database initialization
└── main.py        # Application entry point

alembic/           # Database migrations
Dockerfile
docker-compose.yml
requirements.txt
.env

````

---

## 🔐 Authentication & Roles

Authentication is handled using **JWT tokens** (Access & Refresh).

### Roles

**Admin**
- Full system access
- Manage users, products, suppliers
- View reports and audit logs

**Staff**
- Manage products and inventory
- Perform stock-in / stock-out operations
- View relevant reports

---

## 🔑 API Endpoints Overview

### Auth

- `POST /auth/register` — Register new user  
- `POST /auth/login` — Login & receive tokens  
- `POST /auth/refresh` — Refresh access token  

### Products & Categories

- `POST /products/` — Create product  
- `GET /products/` — List products  
- `PUT /products/{id}` — Update product  
- `DELETE /products/{id}` — Delete product  
- `POST /categories/` — Create category  

### Inventory

- `POST /inventory/stock-in` — Add stock  
- `POST /inventory/stock-out` — Remove stock  
- `GET /inventory/logs` — Inventory history  

### Suppliers

- `POST /suppliers/` — Create supplier  
- `GET /suppliers/` — List suppliers  

### Reports

- `GET /reports/current-stock` — Current inventory  
- `GET /reports/low-stock` — Low stock items  
- `GET /reports/consumption` — Consumption report  

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:password@db:5432/inventory_db
SECRET_KEY=your_secret_key
ACCESS_TOKEN_SECRET_KEY=your_access_secret
REFRESH_TOKEN_SECRET_KEY=your_refresh_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
````

---

## 🐳 Run with Docker (Recommended)

```bash
docker-compose up --build
```

API will be available at:

* [http://localhost:8000](http://localhost:8000)
* Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Run Locally (Without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🧬 Database Migrations

Run migrations locally or inside the container:

```bash
alembic upgrade head
```

---

## 📊 Reporting Capabilities

* Current stock levels
* Low inventory alerts
* Stock movement history
* Consumption trends
* Supplier-based tracking

---

## 🔒 Security Highlights

* Passwords hashed using **Argon2**
* Access & Refresh token rotation
* Role-based authorization enforcement
* Business rule validation at service layer
* CORS hardening support
* Login audit tracking
* Protection against stock underflow

---

## 🎯 Project Objective

This project demonstrates the ability to design and implement a secure, modular, and scalable backend system with:

* Clean architecture principles
* Separation of concerns
* Robust authentication & authorization
* Business logic enforcement
* Database version control
* Production-ready deployment support

It showcases backend engineering skills in API design, security implementation, relational database modeling, and modular system architecture.
