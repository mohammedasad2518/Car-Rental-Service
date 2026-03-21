from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="SpeedRide Car Rental Service",
    description="Complete Car Rental backend — All 20 tasks (Day 1–6)",
    version="1.0.0"
)

# ─────────────── DATA STORE ───────────────

cars = [
    dict(id=1, model="Swift", brand="Maruti", type="Hatchback", price_per_day=1200, fuel_type="Petrol", is_available=True),
    dict(id=2, model="City", brand="Honda", type="Sedan", price_per_day=1800, fuel_type="Petrol", is_available=True),
    dict(id=3, model="Creta", brand="Hyundai", type="SUV", price_per_day=2500, fuel_type="Diesel", is_available=True),
    dict(id=4, model="Fortuner", brand="Toyota", type="SUV", price_per_day=4000, fuel_type="Diesel", is_available=False),
    dict(id=5, model="Model 3", brand="Tesla", type="Luxury", price_per_day=6000, fuel_type="Electric", is_available=True),
    dict(id=6, model="Nexon EV", brand="Tata", type="Hatchback", price_per_day=1500, fuel_type="Electric", is_available=True),
    dict(id=7, model="3 Series", brand="BMW", type="Luxury", price_per_day=7000, fuel_type="Petrol", is_available=True),
    dict(id=8, model="Innova", brand="Toyota", type="Sedan", price_per_day=2200, fuel_type="Diesel", is_available=False),
]

rentals = []
rental_counter, car_counter = 1, 9


# ─────────────── MODELS ───────────────

class RentalRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    car_id: int = Field(..., gt=0)
    days: int = Field(..., gt=0, le=30)
    license_number: str = Field(..., min_length=8)
    insurance: bool = False
    driver_required: bool = False


class NewCar(BaseModel):
    model: str = Field(..., min_length=2)
    brand: str = Field(..., min_length=2)
    type: str = Field(..., min_length=2)
    price_per_day: int = Field(..., gt=0)
    fuel_type: str = Field(..., min_length=2)
    is_available: bool = True


# ─────────────── HELPERS ───────────────

def find_car(car_id: int):
    return next((c for c in cars if c["id"] == car_id), None)


def calculate_rental_cost(price_per_day: int, days: int, insurance: bool, driver_required: bool):
    base = price_per_day * days

    discount = 25 if days >= 15 else 15 if days >= 7 else 0
    discount_amt = round(base * discount / 100)

    after = base - discount_amt
    insurance_cost = (500 * days) if insurance else 0
    driver_cost = (800 * days) if driver_required else 0

    total = after + insurance_cost + driver_cost

    return {
        "base_cost": base,
        "discount_percent": discount,
        "discount_amount": discount_amt,
        "after_discount": after,
        "insurance_cost": insurance_cost,
        "driver_cost": driver_cost,
        "total_cost": total
    }


def filter_cars_logic(type=None, brand=None, fuel_type=None, max_price=None, is_available=None):
    filtered = cars.copy()

    if type:
        filtered = [c for c in filtered if c["type"].lower() == type.lower()]
    if brand:
        filtered = [c for c in filtered if c["brand"].lower() == brand.lower()]
    if fuel_type:
        filtered = [c for c in filtered if c["fuel_type"].lower() == fuel_type.lower()]
    if max_price:
        filtered = [c for c in filtered if c["price_per_day"] <= max_price]
    if is_available is not None:
        filtered = [c for c in filtered if c["is_available"] == is_available]

    return filtered


# ─────────────── ROUTES ───────────────

@app.get("/", tags=["General"])
def home():
    return {"message": "Welcome to SpeedRide Car Rentals"}


@app.get("/cars", tags=["Cars"])
def get_all_cars():
    available = sum(c["is_available"] for c in cars)
    return {"total": len(cars), "available_count": available, "cars": cars}


@app.get("/cars/summary", tags=["Cars"])
def cars_summary():
    total = len(cars)
    available = sum(1 for c in cars if c["is_available"])

    type_map, fuel_map = {}, {}

    for c in cars:
        type_map[c["type"]] = type_map.get(c["type"], 0) + 1
        fuel_map[c["fuel_type"]] = fuel_map.get(c["fuel_type"], 0) + 1

    cheapest = min(cars, key=lambda x: x["price_per_day"])
    expensive = max(cars, key=lambda x: x["price_per_day"])

    return {
        "total_cars": total,
        "available_count": available,
        "breakdown_by_type": type_map,
        "breakdown_by_fuel_type": fuel_map,
        "cheapest_car_per_day": {"model": cheapest["model"], "brand": cheapest["brand"], "price_per_day": cheapest["price_per_day"]},
        "most_expensive_car_per_day": {"model": expensive["model"], "brand": expensive["brand"], "price_per_day": expensive["price_per_day"]}
    }


@app.get("/cars/filter", tags=["Cars"])
def filter_cars_endpoint(
    type: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    fuel_type: Optional[str] = Query(None),
    max_price: Optional[int] = Query(None, gt=0),
    is_available: Optional[bool] = Query(None)
):
    result = filter_cars_logic(type, brand, fuel_type, max_price, is_available)
    if not result:
        raise HTTPException(status_code=404, detail="No cars match the given filters")
    return {"total": len(result), "cars": result}


@app.get("/cars/{car_id}", tags=["Cars"])
def get_car_by_id(car_id: int):
    car = find_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail=f"Car {car_id} not found")
    return car


@app.post("/cars", status_code=201, tags=["Cars"])
def add_car(new_car: NewCar):
    global car_counter

    if any(c["model"].lower() == new_car.model.lower() and c["brand"].lower() == new_car.brand.lower() for c in cars):
        raise HTTPException(status_code=400, detail=f"Car '{new_car.brand} {new_car.model}' already exists")

    new_entry = {"id": car_counter, **new_car.dict()}
    cars.append(new_entry)
    car_counter += 1

    return {"message": "Car added successfully", "car": new_entry}


@app.put("/cars/{car_id}", tags=["Cars"])
def update_car(car_id: int, price_per_day: Optional[int] = Query(None, gt=0), is_available: Optional[bool] = Query(None)):
    car = find_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail=f"Car {car_id} not found")

    if price_per_day:
        car["price_per_day"] = price_per_day
    if is_available is not None:
        car["is_available"] = is_available

    return {"message": "Car updated successfully", "car": car}


@app.delete("/cars/{car_id}", tags=["Cars"])
def delete_car(car_id: int):
    car = find_car(car_id)

    if not car:
        raise HTTPException(status_code=404, detail=f"Car {car_id} not found")

    if any(r["car_id"] == car_id and r["status"] == "active" for r in rentals):
        raise HTTPException(status_code=400, detail="Cannot delete a car with an active rental")

    cars.remove(car)
    return {"message": f"Car {car_id} deleted successfully"}


@app.get("/rentals", tags=["Rentals"])
def get_all_rentals():
    return {"total": len(rentals), "rentals": rentals}


@app.post("/rentals", status_code=201, tags=["Rentals"])
def create_rental(req: RentalRequest):
    global rental_counter

    car = find_car(req.car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    if not car["is_available"]:
        raise HTTPException(status_code=400, detail="Car is not available for rental")

    cost = calculate_rental_cost(car["price_per_day"], req.days, req.insurance, req.driver_required)

    rental = {
        "rental_id": rental_counter,
        "customer_name": req.customer_name,
        "license_number": req.license_number,
        "car_id": req.car_id,
        "car_model": car["model"],
        "car_brand": car["brand"],
        "days": req.days,
        "insurance": req.insurance,
        "driver_required": req.driver_required,
        "status": "active",
        **cost
    }

    car["is_available"] = False
    rentals.append(rental)
    rental_counter += 1

    return {"message": "Rental created successfully", "rental": rental}


@app.post("/return/{rental_id}", tags=["Workflow"])
def return_car(rental_id: int):
    rental = next((r for r in rentals if r["rental_id"] == rental_id), None)

    if not rental:
        raise HTTPException(status_code=404, detail=f"Rental {rental_id} not found")

    if rental["status"] == "returned":
        raise HTTPException(status_code=400, detail="This rental has already been returned")

    rental["status"] = "returned"

    car = find_car(rental["car_id"])
    if car:
        car["is_available"] = True

    return {"message": "Car returned successfully", "rental": rental}