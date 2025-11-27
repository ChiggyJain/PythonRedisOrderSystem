
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

### **4. Redis Features**
Used extensively across the project:

| Feature | Usage |
|--------|--------|
| GET / SET | Product caching, session tokens |
| EXPIRE / TTL | Session token expiry |
| HSET / HGET | Product data |
| Pipeline | Batch Redis operations |
| Streams (XADD / XREADGROUP / XACK) | Order queue processing |
| Sets | Internal unique key store |

### **5. PyTest**
- Session-scoped fixtures  
- Worker integration testing  
- E2E test execution  
- Clean isolation between test runs  

### **6. Swagger UI**
Auto-generated interactive API documentation via FastAPI.

---

## 📘 API Endpoints Overview

### **1️⃣ System Health**
