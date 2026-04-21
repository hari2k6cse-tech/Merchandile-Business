from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class HarvestEntryCreate(BaseModel):
    date: str
    variety: str
    banana_count: int
    weight_kg: Optional[float] = None
    number_of_vehicles: int = 0
    seller_name: str
    expected_amount: float
    actual_amount: Optional[float] = None
    payment_mode: str
    status: str
    notes: Optional[str] = None

class HarvestEntryUpdate(BaseModel):
    date: Optional[str] = None
    variety: Optional[str] = None
    banana_count: Optional[int] = None
    weight_kg: Optional[float] = None
    number_of_vehicles: Optional[int] = None
    seller_name: Optional[str] = None
    expected_amount: Optional[float] = None
    actual_amount: Optional[float] = None
    payment_mode: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class HarvestEntryResponse(BaseModel):
    id: int
    date: str
    variety: str
    banana_count: int
    weight_kg: Optional[float]
    number_of_vehicles: int
    seller_name: str
    expected_amount: float
    actual_amount: Optional[float]
    payment_mode: str
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    profit_loss: float = 0

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None


class SellerPaymentCreate(BaseModel):
    amount_paid: float
    payment_date: str
    notes: Optional[str] = None


class SellerPaymentResponse(BaseModel):
    id: int
    seller_name: str
    amount_paid: float
    payment_date: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SellerSummary(BaseModel):
    seller_name: str
    total_entries: int
    total_expected: float
    total_paid: float
    pending_amount: float
    status: str
    entries: List[HarvestEntryResponse]
    payments: List[SellerPaymentResponse]
