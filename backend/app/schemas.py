from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Image Schemas ---
class ListingImage(BaseModel):
    id: int
    file_path: str
    is_primary: bool

    class Config:
        from_attributes = True

# --- Listing Schemas ---
class ListingBase(BaseModel):
    title: str
    description: str
    category: str
    condition: str
    daily_rate: float
    deposit: float
    pickup_location: str

class ListingCreate(ListingBase):
    pass

class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = None
    daily_rate: Optional[float] = None
    deposit: Optional[float] = None
    pickup_location: Optional[str] = None
    status: Optional[str] = None

class Listing(ListingBase):
    id: int
    owner_id: int
    status: str
    created_at: datetime
    images: List[ListingImage] = []

    class Config:
        from_attributes = True

# --- Booking Schemas ---
class BookingBase(BaseModel):
    start_date: datetime
    end_date: datetime

class BookingCreate(BookingBase):
    listing_id: int

class Booking(BookingBase):
    id: int
    listing_id: int
    renter_id: int
    rental_fee: float
    service_fee: float
    deposit: float
    total_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Payment Schemas ---
class PaymentProcess(BaseModel):
    amount: float
    provider_token: str

class Payment(BaseModel):
    id: int
    booking_id: int
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
