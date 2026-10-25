from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import os
import shutil
import json

from . import models, schemas, auth, database, ai

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="RentEase API")

UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Authentication Endpoints ---

@app.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = auth.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=models.UserRole.user.value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.get_user(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

# --- Listing Endpoints ---

@app.post("/listings", response_model=schemas.Listing)
def create_listing(listing: schemas.ListingCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    # Generate actual embedding for semantic search using sentence-transformers
    text_to_embed = f"{listing.title} {listing.description} {listing.category}"
    actual_embedding = ai.get_embedding(text_to_embed)
    embedding_str = json.dumps(actual_embedding)

    db_listing = models.Listing(**listing.model_dump(), owner_id=current_user.id, embedding=embedding_str)
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

@app.get("/listings", response_model=list[schemas.Listing])
def read_listings(skip: int = 0, limit: int = 100, search: str = None, category: str = None, db: Session = Depends(database.get_db)):
    query = db.query(models.Listing).filter(models.Listing.status == models.ListingStatus.active.value)
    if search:
        query = query.filter(models.Listing.title.contains(search) | models.Listing.description.contains(search))
    if category:
        query = query.filter(models.Listing.category == category)
    return query.offset(skip).limit(limit).all()

@app.get("/listings/{listing_id}", response_model=schemas.Listing)
def read_listing(listing_id: int, db: Session = Depends(database.get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@app.post("/listings/{listing_id}/images", response_model=schemas.ListingImage)
def upload_listing_image(listing_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing or listing.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Listing not found or not owned by user")

    file_path = os.path.join(UPLOAD_DIR, f"{listing_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_image = models.ListingImage(listing_id=listing_id, file_path=file_path)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

# --- Booking Endpoints ---

@app.post("/bookings", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    listing = db.query(models.Listing).filter(models.Listing.id == booking.listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    # Overlap check
    overlapping_bookings = db.query(models.Booking).filter(
        models.Booking.listing_id == booking.listing_id,
        models.Booking.status.in_([models.BookingStatus.approved.value, models.BookingStatus.active.value]),
        models.Booking.start_date < booking.end_date,
        models.Booking.end_date > booking.start_date
    ).first()

    if overlapping_bookings:
        raise HTTPException(status_code=400, detail="Dates are not available")

    days = (booking.end_date - booking.start_date).days
    if days <= 0: days = 1 # Handle same-day as 1 day

    rental_fee = listing.daily_rate * days
    service_fee = rental_fee * 0.1 # 10% service fee mock
    total_amount = rental_fee + service_fee + listing.deposit

    db_booking = models.Booking(
        **booking.model_dump(),
        renter_id=current_user.id,
        rental_fee=rental_fee,
        service_fee=service_fee,
        deposit=listing.deposit,
        total_amount=total_amount
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

# --- Sandbox Payment Endpoint ---

@app.post("/bookings/{booking_id}/pay", response_model=schemas.Payment)
def mock_payment(booking_id: int, payment_data: schemas.PaymentProcess, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking or booking.renter_id != current_user.id:
        raise HTTPException(status_code=404, detail="Booking not found")

    if payment_data.amount != booking.total_amount:
        raise HTTPException(status_code=400, detail="Payment amount does not match total amount")

    # Mock Sandbox Payment Success
    db_payment = models.Payment(
        booking_id=booking.id,
        amount=payment_data.amount,
        status=models.PaymentStatus.completed.value,
        provider_id="sandbox_" + payment_data.provider_token
    )
    booking.status = models.BookingStatus.approved.value # Auto approve on mock payment
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment
