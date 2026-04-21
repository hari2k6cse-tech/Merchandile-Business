from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine, Base, get_db
from models import HarvestEntry, SellerPayment
from schemas import (
    HarvestEntryCreate, HarvestEntryUpdate, HarvestEntryResponse,
    SellerPaymentCreate, SellerPaymentResponse, SellerSummary,
    LoginRequest, LoginResponse
)
from typing import List
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Banana Merchandise Portal API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.options("/{full_path:path}")
async def preflight_handler(full_path: str):
    return JSONResponse(status_code=200, content={"message": "OK"})

# ==================== HELPER FUNCTIONS ====================

def serialize_entry(entry: HarvestEntry) -> HarvestEntryResponse:
    """Build a response payload with computed profit/loss."""
    return HarvestEntryResponse(
        id=entry.id,
        date=entry.date,
        variety=entry.variety,
        banana_count=entry.banana_count,
        weight_kg=entry.weight_kg,
        number_of_vehicles=entry.number_of_vehicles,
        seller_name=entry.seller_name,
        expected_amount=entry.expected_amount,
        actual_amount=entry.actual_amount,
        payment_mode=entry.payment_mode,
        status=entry.status,
        notes=entry.notes,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
        profit_loss=(entry.actual_amount or 0) - entry.expected_amount,
    )

def calculate_seller_status(total_paid: float, total_expected: float) -> str:
    """Calculate seller payment status"""
    if total_paid >= total_expected:
        return "முழுமையாக பணம் பெறப்பட்டது"
    elif total_paid > 0:
        return "ஓரளவு பணம் பெறப்பட்டது"
    else:
        return "வழங்கப்பட்டது"

def update_seller_entry_statuses(db: Session, seller_name: str):
    """Update all entries for a seller based on payment status"""
    # Get all entries for this seller
    entries = db.query(HarvestEntry).filter(
        HarvestEntry.seller_name.ilike(f"%{seller_name}%")
    ).all()
    
    if not entries:
        return
    
    # Calculate totals
    total_expected = sum(e.expected_amount for e in entries)
    
    # Get total paid
    payments = db.query(SellerPayment).filter(
        SellerPayment.seller_name.ilike(f"%{seller_name}%")
    ).all()
    total_paid = sum(p.amount_paid for p in payments)
    
    # Determine status
    new_status = calculate_seller_status(total_paid, total_expected)
    
    # Update all entries
    for entry in entries:
        entry.status = new_status
    
    db.commit()

# ==================== AUTHENTICATION ====================

@app.post("/api/login", response_model=LoginResponse)
def login(credentials: LoginRequest):
    if credentials.username == "hari" and credentials.password == "hari":
        return LoginResponse(
            success=True,
            message="உள்நுழைவு வெற்றிகரமாக",
            token="hari_token_12345"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="தவறான பயனர்பெயர் அல்லது கடவுச்சொல்"
        )

# ==================== HARVEST ENTRY CRUD ====================

@app.post("/api/entries", response_model=HarvestEntryResponse)
def create_entry(entry: HarvestEntryCreate, db: Session = Depends(get_db)):
    """Create new harvest entry - status auto-set to வழங்கப்பட்டது"""
    try:
        db_entry = HarvestEntry(**entry.dict())
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        
        # Check if this seller now has payments, update status if needed
        update_seller_entry_statuses(db, entry.seller_name)
        db.refresh(db_entry)
        
        return serialize_entry(db_entry)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/entries", response_model=List[HarvestEntryResponse])
def get_all_entries(db: Session = Depends(get_db)):
    """Get all harvest entries"""
    try:
        entries = db.query(HarvestEntry).all()
        return [serialize_entry(e) for e in entries]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/entries/{entry_id}", response_model=HarvestEntryResponse)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    """Get single harvest entry"""
    try:
        entry = db.query(HarvestEntry).filter(HarvestEntry.id == entry_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="பதிவு காணப்படவில்லை")
        return serialize_entry(entry)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/entries/{entry_id}", response_model=HarvestEntryResponse)
def update_entry(entry_id: int, entry: HarvestEntryUpdate, db: Session = Depends(get_db)):
    """Update harvest entry"""
    try:
        db_entry = db.query(HarvestEntry).filter(HarvestEntry.id == entry_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="பதிவு காணப்படவில்லை")
        
        update_data = entry.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_entry, field, value)
        
        db_entry.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_entry)
        
        return serialize_entry(db_entry)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/entries/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    """Delete harvest entry"""
    try:
        db_entry = db.query(HarvestEntry).filter(HarvestEntry.id == entry_id).first()
        if not db_entry:
            raise HTTPException(status_code=404, detail="பதிவு காணப்படவில்லை")
        
        db.delete(db_entry)
        db.commit()
        
        return {"message": "பதிவு நீக்கப்பட்டது"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# ==================== SELLER ENDPOINTS ====================

@app.get("/api/sellers")
def get_all_sellers(db: Session = Depends(get_db)):
    """Get all unique sellers with aggregated stats"""
    try:
        # Get all unique sellers
        sellers = db.query(HarvestEntry.seller_name).distinct().all()
        result = []
        
        for (seller_name,) in sellers:
            # Get entries
            entries = db.query(HarvestEntry).filter(
                HarvestEntry.seller_name.ilike(f"%{seller_name}%")
            ).all()
            
            # Get payments
            payments = db.query(SellerPayment).filter(
                SellerPayment.seller_name.ilike(f"%{seller_name}%")
            ).all()
            
            total_expected = sum(e.expected_amount for e in entries)
            total_paid = sum(p.amount_paid for p in payments)
            pending = total_expected - total_paid
            status_val = calculate_seller_status(total_paid, total_expected)
            
            result.append({
                "seller_name": seller_name,
                "total_entries": len(entries),
                "total_expected": total_expected,
                "total_paid": total_paid,
                "pending_amount": pending,
                "status": status_val
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/sellers/{seller_name}/summary", response_model=SellerSummary)
def get_seller_summary(seller_name: str, db: Session = Depends(get_db)):
    """Get detailed summary for a seller"""
    try:
        entries = db.query(HarvestEntry).filter(
            HarvestEntry.seller_name.ilike(f"%{seller_name}%")
        ).all()
        
        payments = db.query(SellerPayment).filter(
            SellerPayment.seller_name.ilike(f"%{seller_name}%")
        ).all()
        
        total_expected = sum(e.expected_amount for e in entries)
        total_paid = sum(p.amount_paid for p in payments)
        pending = total_expected - total_paid
        status_val = calculate_seller_status(total_paid, total_expected)
        
        return SellerSummary(
            seller_name=seller_name,
            total_entries=len(entries),
            total_expected=total_expected,
            total_paid=total_paid,
            pending_amount=pending,
            status=status_val,
            entries=[HarvestEntryResponse.from_orm(e) for e in entries],
            payments=[SellerPaymentResponse.from_orm(p) for p in payments]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/sellers/{seller_name}/payment", response_model=SellerPaymentResponse)
def record_seller_payment(seller_name: str, payment: SellerPaymentCreate, db: Session = Depends(get_db)):
    """Record a payment from a seller"""
    try:
        if payment.amount_paid <= 0:
            raise HTTPException(status_code=400, detail="தொகை பூஜ்ஜியத்தை விட அதிகமாக இருக்க வேண்டும்")
        
        # Get seller's entries to validate pending amount
        entries = db.query(HarvestEntry).filter(
            HarvestEntry.seller_name.ilike(f"%{seller_name}%")
        ).all()
        
        payments = db.query(SellerPayment).filter(
            SellerPayment.seller_name.ilike(f"%{seller_name}%")
        ).all()
        
        total_expected = sum(e.expected_amount for e in entries)
        total_paid = sum(p.amount_paid for p in payments)
        pending = total_expected - total_paid
        
        if payment.amount_paid > pending:
            raise HTTPException(status_code=400, detail="தொகை நிலுவையை தாண்ட முடியாது")
        
        # Create payment record
        db_payment = SellerPayment(
            seller_name=seller_name,
            amount_paid=payment.amount_paid,
            payment_date=payment.payment_date,
            notes=payment.notes
        )
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        
        # Update all entries for this seller
        update_seller_entry_statuses(db, seller_name)
        
        return SellerPaymentResponse.from_orm(db_payment)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/sellers/{seller_name}/payments", response_model=List[SellerPaymentResponse])
def get_seller_payments(seller_name: str, db: Session = Depends(get_db)):
    """Get payment history for a seller"""
    try:
        payments = db.query(SellerPayment).filter(
            SellerPayment.seller_name.ilike(f"%{seller_name}%")
        ).all()
        return [SellerPaymentResponse.from_orm(p) for p in payments]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/sellers/{seller_name}/payment/{payment_id}")
def delete_seller_payment(seller_name: str, payment_id: int, db: Session = Depends(get_db)):
    """Delete a payment record"""
    try:
        payment = db.query(SellerPayment).filter(SellerPayment.id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="பணம் பெற்ற பதிவு காணப்படவில்லை")
        
        db.delete(payment)
        db.commit()
        
        # Update seller statuses
        update_seller_entry_statuses(db, seller_name)
        
        return {"message": "பணம் பெற்ற பதிவு நீக்கப்பட்டது"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# ==================== ANALYTICS ====================

@app.get("/api/analytics/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    """Get dashboard summary stats"""
    try:
        entries = db.query(HarvestEntry).all()
        payments = db.query(SellerPayment).all()
        
        total_entries = len(entries)
        total_expected = sum(e.expected_amount for e in entries)
        total_actual = sum((e.actual_amount or 0) for e in entries)
        total_paid = sum(p.amount_paid for p in payments)
        total_pending = total_expected - total_paid
        net_profit_loss = total_actual - total_expected
        
        return {
            "total_entries": total_entries,
            "total_expected": total_expected,
            "total_paid": total_paid,
            "total_pending": total_pending,
            "expected_revenue": total_expected,
            "actual_received": total_actual,
            "net_profit_loss": net_profit_loss
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/seller-chart-data")
def get_seller_chart_data(db: Session = Depends(get_db)):
    """Get chart data for sellers - pending vs paid"""
    try:
        sellers = db.query(HarvestEntry.seller_name).distinct().all()
        
        data = []
        for (seller_name,) in sellers:
            entries = db.query(HarvestEntry).filter(
                HarvestEntry.seller_name.ilike(f"%{seller_name}%")
            ).all()
            payments = db.query(SellerPayment).filter(
                SellerPayment.seller_name.ilike(f"%{seller_name}%")
            ).all()
            
            total_expected = sum(e.expected_amount for e in entries)
            total_paid = sum(p.amount_paid for p in payments)
            
            data.append({
                "seller": seller_name,
                "expected": total_expected,
                "paid": total_paid,
                "pending": total_expected - total_paid
            })
        
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/chart-data")
def get_chart_data(db: Session = Depends(get_db)):
    """Get chart data in the shape expected by the current frontend."""
    try:
        entries = db.query(HarvestEntry).order_by(HarvestEntry.date.asc(), HarvestEntry.id.asc()).all()

        return {
            "labels": [f"{entry.date} - {entry.seller_name}" for entry in entries],
            "expected": [entry.expected_amount for entry in entries],
            "actual": [(entry.actual_amount or 0) for entry in entries]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/variety-data")
def get_variety_chart_data(db: Session = Depends(get_db)):
    """Get chart data for banana varieties"""
    try:
        varieties = db.query(HarvestEntry.variety, 
                            func.sum(HarvestEntry.banana_count).label("total_count")
                           ).group_by(HarvestEntry.variety).all()
        
        return [{"variety": v[0], "count": v[1] or 0} for v in varieties]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/status-breakdown")
def get_status_breakdown(db: Session = Depends(get_db)):
    """Get status distribution"""
    try:
        entries = db.query(HarvestEntry).all()
        
        status_counts = {}
        for entry in entries:
            status_counts[entry.status] = status_counts.get(entry.status, 0) + 1
        
        items = [{"status": k, "count": v} for k, v in status_counts.items()]
        return {
            "labels": [item["status"] for item in items],
            "data": [item["count"] for item in items],
            "items": items
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== HEALTH CHECK ====================

@app.get("/api/health")
def health_check():
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
