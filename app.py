import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ============================================================
# DATABASE SETUP
# ============================================================

DB_NAME = "student_housing.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Housing listings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            rent INTEGER NOT NULL,
            location TEXT NOT NULL,
            description TEXT
        )
    """)

    # Roommate profiles table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS roommates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            major TEXT NOT NULL,
            budget INTEGER NOT NULL,
            lifestyle TEXT
        )
    """)

    conn.commit()

# ============================================================
# MODELS
# ============================================================

class ListingCreate(BaseModel):
    title: str
    rent: int
    location: str
    description: str

class ListingUpdate(BaseModel):
    title: str
    rent: int
    location: str
    description: str

class RoommateCreate(BaseModel):
    name: str
    major: str
    budget: int
    lifestyle: str

class RoommateUpdate(BaseModel):
    name: str
    major: str
    budget: int
    lifestyle: str

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(title="Student Housing & Roommate Finder API")

@app.on_event("startup")
def startup():
    init_db()

# ============================================================
# HOUSING LISTINGS ENDPOINTS
# ============================================================

@app.post("/listings", status_code=201)
def create_listing(listing: ListingCreate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO listings (title, rent, location, description) VALUES (?, ?, ?, ?)",
        (listing.title, listing.rent, listing.location, listing.description)
    )
    conn.commit()
    return {"id": cur.lastrowid, **listing.dict()}

@app.get("/listings")
def get_listings():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, rent, location, description FROM listings")
    rows = cur.fetchall()
    return [
        {"id": r[0], "title": r[1], "rent": r[2], "location": r[3], "description": r[4]}
        for r in rows
    ]

@app.put("/listings/{listing_id}")
def update_listing(listing_id: int, listing: ListingUpdate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE listings SET title = ?, rent = ?, location = ?, description = ? WHERE id = ?",
        (listing.title, listing.rent, listing.location, listing.description, listing_id)
    )
    conn.commit()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Listing not found")

    return {"id": listing_id, **listing.dict()}

@app.delete("/listings/{listing_id}", status_code=204)
def delete_listing(listing_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM listings WHERE id = ?", (listing_id,))
    conn.commit()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Listing not found")
    return

# ============================================================
# ROOMMATE PROFILES ENDPOINTS
# ============================================================

@app.post("/roommates", status_code=201)
def create_roommate(profile: RoommateCreate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO roommates (name, major, budget, lifestyle) VALUES (?, ?, ?, ?)",
        (profile.name, profile.major, profile.budget, profile.lifestyle)
    )
    conn.commit()
    return {"id": cur.lastrowid, **profile.dict()}

@app.get("/roommates")
def get_roommates():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, major, budget, lifestyle FROM roommates")
    rows = cur.fetchall()
    return [
        {"id": r[0], "name": r[1], "major": r[2], "budget": r[3], "lifestyle": r[4]}
        for r in rows
    ]

@app.put("/roommates/{roommate_id}")
def update_roommate(roommate_id: int, profile: RoommateUpdate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE roommates SET name = ?, major = ?, budget = ?, lifestyle = ? WHERE id = ?",
        (profile.name, profile.major, profile.budget, profile.lifestyle, roommate_id)
    )
    conn.commit()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Roommate not found")

    return {"id": roommate_id, **profile.dict()}

@app.delete("/roommates/{roommate_id}", status_code=204)
def delete_roommate(roommate_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM roommates WHERE id = ?", (roommate_id,))
    conn.commit()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Roommate not found")
    return
