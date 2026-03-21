# Car Rental Service

A fully functional **Car Rental Service backend** built using **FastAPI** as part of my internship final project at **Innomatics Research Labs**.

This project covers all concepts from Day 1 to Day 6 — GET APIs, POST with Pydantic validation, helper functions, CRUD operations, multi-step workflows, search, sorting, and pagination.


## 🚀 How to Run

```bash
# Step 1 — Install dependencies
pip install -r requirements.txt

# Step 2 — Start the server
uvicorn main:app --reload

# Step 3 — Open Swagger UI
http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```
fastapi-car-rental-service/
│
├── main.py              # All API endpoints
├── requirements.txt     # Dependencies
├── README.md            # Project documentation
└── screenshots/         # Swagger screenshots for all 20 questions
```

---

## ✨ Features Implemented

| Day | Concept | What I Built |
|-----|---------|-------------|
| Day 1 | GET APIs | Home route, list all cars, get by ID, rentals, summary stats |
| Day 2 | POST + Pydantic | RentalRequest with field validation, error handling |
| Day 3 | Helper Functions | `find_car()`, `calculate_rental_cost()`, `filter_cars_logic()` |
| Day 4 | CRUD Operations | Add car, update car, delete car with business rules |
| Day 5 | Multi-step Workflow | Rent car → Return car → Rental history |
| Day 6 | Search, Sort, Pagination | Keyword search, sorting, pagination, combined browse |

---

## 📋 All 20 API Endpoints

### 🟢 Day 1 — GET APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/cars` | List all cars with available count |
| GET | `/cars/{car_id}` | Get a specific car by ID |
| GET | `/rentals` | List all rentals |
| GET | `/cars/summary` | Stats — type breakdown, fuel breakdown, cheapest & most expensive |

### 🔵 Day 2 + Day 3 — POST & Helpers

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rentals` | Create a rental with full cost breakdown |

**Pydantic Validation Rules:**
- `customer_name` — min 2 characters
- `days` — must be between 1 and 30
- `license_number` — min 8 characters
- `insurance` — bool (default False)
- `driver_required` — bool (default False)

**Cost Calculation Logic:**
- 7+ days → **15% discount**
- 15+ days → **25% discount**
- Insurance → **+₹500/day**
- Driver → **+₹800/day**

### 🟡 Day 3 — Filter

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cars/filter` | Filter by type, brand, fuel_type, max_price, is_available |

### 🟠 Day 4 — CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/cars` | Add new car (rejects duplicate model+brand) |
| PUT | `/cars/{car_id}` | Update price or availability |
| DELETE | `/cars/{car_id}` | Delete car (blocked if active rental exists) |

### 🩵 Day 5 — Workflow

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/return/{rental_id}` | Return a rented car |
| GET | `/rentals/{rental_id}` | Get rental by ID |
| GET | `/rentals/active` | View all active rentals |
| GET | `/rentals/by-car/{car_id}` | Rental history for a specific car |
| GET | `/cars/unavailable` | All currently unavailable cars |

### 🔴 Day 6 — Search, Sort, Pagination

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cars/search` | Keyword search across model, brand, type |
| GET | `/cars/sort` | Sort by price_per_day, brand, or type |
| GET | `/cars/page` | Paginate cars with total_pages |
| GET | `/rentals/search` | Search rentals by customer name |
| GET | `/rentals/sort` | Sort rentals by total_cost or days |
| GET | `/rentals/page` | Paginate rentals |
| GET | `/cars/browse` | Combined — keyword + filter + sort + paginate |

---

## 🧪 Sample Data

The project comes with **8 pre-loaded cars:**

| Brand | Model | Type | Fuel | Price/Day |
|-------|-------|------|------|-----------|
| Maruti | Swift | Hatchback | Petrol | ₹1,200 |
| Honda | City | Sedan | Petrol | ₹1,800 |
| Hyundai | Creta | SUV | Diesel | ₹2,500 |
| Toyota | Fortuner | SUV | Diesel | ₹4,000 |
| Tesla | Model 3 | Luxury | Electric | ₹6,000 |
| Tata | Nexon EV | Hatchback | Electric | ₹1,500 |
| BMW | 3 Series | Luxury | Petrol | ₹7,000 |
| Toyota | Innova | Sedan | Diesel | ₹2,200 |

---

## 🙏 Acknowledgement

Thanks to **Innomatics Research Labs** for the structured FastAPI internship training. This project helped me understand how to design real-world REST APIs, structure backend systems, and implement complete application workflows.

