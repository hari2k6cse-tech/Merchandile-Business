from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from database import Base
from datetime import datetime

class HarvestEntry(Base):
    __tablename__ = "harvest_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    variety = Column(String, index=True)  # Tamil name
    banana_count = Column(Integer)
    weight_kg = Column(Float, nullable=True)
    number_of_vehicles = Column(Integer, default=0)
    seller_name = Column(String)
    expected_amount = Column(Float)
    actual_amount = Column(Float, nullable=True)
    payment_mode = Column(String)
    status = Column(String)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_profit_loss(self):
        if self.actual_amount is None:
            return 0
        return self.actual_amount - self.expected_amount


class SellerPayment(Base):
    __tablename__ = "seller_payments"

    id = Column(Integer, primary_key=True, index=True)
    seller_name = Column(String, index=True, nullable=False)
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
