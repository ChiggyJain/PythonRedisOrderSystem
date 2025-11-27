
# 🚀 Redis Order System (FastAPI + Redis Streams)

A high-performance backend system built using **FastAPI**, **Redis**, and **PyTest**.  
This project demonstrates real-world backend engineering including Redis caching, Redis Streams-based asynchronous order processing, standardized API responses, and full automated testing.

---

## 🛠️ Tech Stack Used

### **1. FastAPI Framework**
- High-performance async web framework  
- Automatic Swagger UI documentation  
- Dependency Injection support  

### **2. Pydantic Models**
- Strong request validation  
- Standard response errors on validation failure  
- Used only for handling API input payloads  

### **3. Custom Exception Handling**
- All API errors return a **Standard Response Format**  
- Global error handlers implemented

### **4. Custom Response Handling**
- All API return a **Standard Response Format**  

### **5. Redis Features**
Used extensively across the project:

| Feature | Usage |
|--------|--------|
| GET / SET | Product caching, session tokens |
| EXPIRE / TTL | Session token expiry |
| HSET / HGET | Product data |
| Pipeline | Batch Redis operations |
| Streams (XADD / XREADGROUP / XACK) | Order queue processing |
| Sets | Internal unique key store |

### **6. PyTest**
- Session-scoped fixtures  
- Worker integration testing  
- E2E test execution  
- Clean isolation between test runs  

### **7. Swagger UI**
Auto-generated interactive API documentation via FastAPI.
URL: http://127.0.0.1:8000/docs

---

## 📘 API Endpoints Overview

### **1️⃣ System Health**
GET /system-health
Checks if the backend is running.

### **2️⃣ User Login (Generates Session Token)**
POST /users/login
- Validates user credentials  
- Generates a session token stored in Redis (No JWT)  
- Token TTL controlled by Redis  
- Returns token in standard response format  

### **3️⃣ Get All Products**
GET /products
Headers:
Authorization: Bearer <token>

### **4️⃣ Get Product by ID**
GET /products/{product_id}
Headers:
Authorization: Bearer <token>

### **5️⃣ Set Product Stock**
POST /products/setstock
Headers:
Authorization: Bearer <token>

### **6️⃣ Place Order (Redis Stream Event)**
POST /orders/place-order
Headers:
Authorization: Bearer <token>
This:
- Pushes an order event into a Redis Stream  
- Background worker listens and processes orders  
- Worker acknowledges processed messages


---

## ⚙️ Installation (Local Machine)

### **1️⃣ Install System Requirements**
- Python **3.12**
- Redis Server (latest stable)

---

## 🐍 Setup Virtual Environment

```bash python3 -m venv venv

Activate environment: source venv/bin/activate
Install project dependencies: pip install -r requirements.txt
▶️ Running the Project
Terminal 1 – Start FastAPI Application
uvicorn app.main:app
Terminal 2 – Start Background Redis Worker
python -c "from app.workers.order_placed_worker import runOrderPlacedStreamConsumerGroupWorker1; runOrderPlacedStreamConsumerGroupWorker1()"
pytest -v tests/test_all_things_in_one_way.py \
    --disable-warnings \
    --maxfail=0 \
    -W ignore::DeprecationWarning \
    -s
