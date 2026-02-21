# Inventory Management API (FastAPI + PostgreSQL)

A production-style **API-first** inventory management system built with **FastAPI**, **PostgreSQL**, and **JWT authentication**.  
Designed to practice clean architecture, business rules, reporting queries (aggregations), and security hardening.

---

## ✨ Features

### ✅ Authentication & Authorization
- JWT-based auth (**Access Token + Refresh Token**)
- Password hashing with **Argon2**
- Role-Based Access Control (RBAC)
  - **admin**: manage users/products/categories/suppliers + access reports & audits
  - **staff**: can only register inventory movements (stock IN/OUT)

### ✅ Inventory Management (Ledger-Based)
- Stock is NOT stored directly on products
- Current stock is computed from the **inventory ledger**:
  - `current_stock = SUM(IN) - SUM(OUT)`
- Stock movements:
  - **Stock IN** (optionally linked to a supplier)
  - **Stock OUT** (validated against current stock)

### ✅ Core Modules
- Users
- Categories
- Products
- Inventory (IN/OUT + history)
- Suppliers
- Reports
- Audit logs

---

## 🧠 Business Rules (Validation)
- Prevent OUT transactions greater than current stock
- Prevent duplicate SKU
- Prevent deleting categories that contain products
- Prevent deleting products that already have inventory transactions
- Prevent zero/negative quantity in stock movements

---

## 🔐 Security Enhancements (Hardened)
This project includes practical security controls often seen in real systems:

1. **CORS Hardening**
   - restricted origins/methods/headers
   - `allow_credentials` disabled (when not required)

2. **Password Policy Enforcement**
   - minimum length
   - must include letters + digits
   - rejects weak passwords patterns

3. **Email Enumeration Prevention**
   - login/refresh errors are normalized (same response for invalid email/password)

4. **Login Auditing**
   - all login attempts are stored with metadata (IP/User-Agent)
   - success/failure tracked for monitoring

5. **Account Lockout**
   - temporary lock after repeated failed attempts (mitigates brute force)

6. **Refresh Token Rotation + Reuse Detection**
   - refresh tokens are stored **hashed**
   - each refresh rotates the token
   - reuse of an old token triggers:
     - revocation of all active refresh tokens
     - audit log event

---

## 🔎 Filtering / Sorting / Pagination

### Products
`GET /products`
- Filtering:
  - `category_id`
  - `name` (partial match)
  - `search` (name search)
- Sorting:
  - `sort_by` + `sort_order`
- Pagination:
  - `page`, `page_size` (or offset-based where applicable)

### Inventory History
`GET /inventory/history`
- Filters:
  - `change_type` (IN / OUT)
  - `product_id`
  - `user_id`
  - `supplier_id`
  - `start_date`, `end_date`
- Sorting:
  - by `created_at`, `quantity`, etc.
- Pagination:
  - `page`, `page_size`

---

## 🧾 Reports
`/reports/*` endpoints provide SQL aggregation practice such as:
- Current stock per product (IN/OUT/current_stock)
- Low-stock items (based on `min_quantity`)
- Time-range movement report
- Top inbound / top consumption

---

## 🧱 Tech Stack
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Pydantic**
- **Argon2**
- **JWT (Access + Refresh)**

---

## 🚀 Run Locally

### 1) Create `.env`
Example:
```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/inventory_db
JWT_SECRET_KEY=CHANGE_ME
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
````

### 2) Docker

```bash
docker-compose up --build
```

### 3) API Docs

* Swagger UI: `/docs`
* ReDoc: `/redoc`

---

## ✅ Quick Test Scenario

1. Register admin
2. Create category
3. Create product (unique SKU)
4. Stock IN (with supplier)
5. Stock OUT (must not exceed stock)
6. Check inventory history + reports
7. Verify staff cannot create products/categories

---

## 📌 Project Structure

```
app/
 ├── core/          # config, db dependencies, security, password policy
 ├── auth/
 ├── users/
 ├── categories/
 ├── products/
 ├── inventory/
 ├── suppliers/
 ├── reports/
 ├── audit/
 └── main.py
```

---

## 📄 License

MIT (or your preferred license)

```
