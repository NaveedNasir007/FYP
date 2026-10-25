from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from .database import Base

class UserRole(str, enum.Enum):
    user = "user"
    owner = "owner"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default=UserRole.user.value) # user, owner, admin
    created_at = Column(DateTime, default=datetime.utcnow)

    listings = relationship("Listing", back_populates="owner")
    bookings = relationship("Booking", back_populates="renter")


class ListingStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    deleted = "deleted"

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(String)
    category = Column(String, index=True)
    condition = Column(String)
    daily_rate = Column(Float)
    deposit = Column(Float)
    pickup_location = Column(String)
    status = Column(String, default=ListingStatus.active.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    embedding = Column(String, nullable=True) # Storing as JSON string since we use SQLite

    owner = relationship("User", back_populates="listings")
    images = relationship("ListingImage", back_populates="listing")
    bookings = relationship("Booking", back_populates="listing")

class ListingImage(Base):
    __tablename__ = "listing_images"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    file_path = Column(String)
    is_primary = Column(Boolean, default=False)

    listing = relationship("Listing", back_populates="images")

class BookingStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    renter_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    rental_fee = Column(Float)
    service_fee = Column(Float)
    deposit = Column(Float)
    total_amount = Column(Float)
    status = Column(String, default=BookingStatus.pending.value)
    created_at = Column(DateTime, default=datetime.utcnow)

    listing = relationship("Listing", back_populates="bookings")
    renter = relationship("User", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)

class PaymentStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True)
    amount = Column(Float)
    status = Column(String, default=PaymentStatus.pending.value)
    provider_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    booking = relationship("Booking", back_populates="payment")
