from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import HarvestEntry
from schemas import (
    HarvestEntryCreate, HarvestEntryUpdate, HarvestEntryResponse,
    LoginRequest, LoginResponse
)
from typing import List
import json

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Banana Merchandise Portal API")

# CORS middleware - Allow all origins including file://
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Options handler for preflight requests
@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    return JSONResponse(status_code=200, content={"message": "OK"})

# ==================== AUTHENTICATION ====================

@app.post("/api/login", response_model=LoginResponse)
def login(credentials: LoginRequest):
    """Simple login endpoint"""
    if credentials.username == "Balu" and credentials.password == "Balu":
        return LoginResponse(
            success=True,
            message="Login successful",
            token="balu_token_12345"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

# ==================== HARVEST ENTRY CRUD ====================

@app.post("/api/entries", response_model=HarvestEntryResponse)
def create_entry(entry: HarvestEntryCreate, db: Session = Depends(get_db)):
    """Create new harvest entry"""
    try:
        db_entry = HarvestEntry(**entry.dict())
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        
        response = HarvestEntryResponse.from_orm(db_entry)
        response.profit_loss = db_entry.get_profit_loss()
        return response
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/entries", response_model=List[HarvestEntryResponse])
def get_all_entries(db: Session = Depends(get_db)):
    """Get all harvest entries"""
    try:
        entries = db.query(HarvestEntry).all()
        results = []
        for entry in entries:
            response = HarvestEntryResponse.from_orm(entry)
            response.profit_loss = entry.get_profit_loss()
            results.append(response)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/entries/{entry_id}", response_model=HarvestEntryResponse)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    """Get single harvest entry"""
    try:
        entry = db.query(HarvestEntry).filter(HarvestEntry.id == entry_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        response = HarvestEntryResponse.from_orm(entry)
        response.profit_loss = entry.get_profit_loss()
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/entries/{entry_id}", response_model=HarvestEntryResponse)
def update_entry(entry_id: int, entry: HarvestEntryUpdate, db: Session = Depends(get_db)):
    """Update harvest entry"""
    try:
        db_entry = db.query(HarvestEntry).filter(HarvestEntry.id == entry_id).first()
        if not db_entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        update_data = entry.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_entry, field, value)
        
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        
        response = HarvestEntryResponse.from_orm(db_entry)
        response.profit_loss = db_entry.get_profit_loss()
        return response
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/entries/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    """Delete harvest entry"""
    try:
        db_entry = db.query(HarvestEntry).filter(HarvestEntry.id == entry_id).first()
        if not db_entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        db.delete(db_entry)
        db.commit()
        return {"message": "Entry deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# ==================== ANALYTICS ====================

@app.get("/api/analytics/summary")
def get_summary(db: Session = Depends(get_db)):
    """Get summary analytics"""
    try:
        entries = db.query(HarvestEntry).all()
        
        total_entries = len(entries)
        total_expected = sum(e.expected_amount or 0 for e in entries)
        total_actual = sum(e.actual_amount or 0 for e in entries)
        net_profit_loss = total_actual - total_expected
        
        return {
            "total_entries": total_entries,
            "expected_revenue": round(total_expected, 2),
            "actual_received": round(total_actual, 2),
            "net_profit_loss": round(net_profit_loss, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/chart-data")
def get_chart_data(db: Session = Depends(get_db)):
    """Get chart data for expected vs actual"""
    try:
        entries = db.query(HarvestEntry).order_by(HarvestEntry.id.desc()).limit(10).all()
        entries = list(reversed(entries))  # Reverse to show chronologically
        
        return {
            "labels": [f"Entry {e.id}" for e in entries],
            "expected": [e.expected_amount or 0 for e in entries],
            "actual": [e.actual_amount or 0 for e in entries],
            "dates": [e.date for e in entries]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/status-breakdown")
def get_status_breakdown(db: Session = Depends(get_db)):
    """Get status distribution"""
    try:
        entries = db.query(HarvestEntry).all()
        
        status_counts = {}
        for entry in entries:
            status = entry.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "labels": list(status_counts.keys()),
            "data": list(status_counts.values())
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== HEALTH CHECK ====================

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
