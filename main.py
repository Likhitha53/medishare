
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from uuid import uuid4

app = FastAPI(
    title="MediShare Medicine Donation Portal",
    description="API for managing medicine donations",
    version="1.0"
)

# Temporary storage
donations = {}


# Donation model
class Donation(BaseModel):
    donor_name: str = Field(min_length=2)
    medicine_name: str = Field(min_length=2)
    quantity: int = Field(gt=0)
    expiry_date: date
    location: str
    contact: str
    description: Optional[str] = None


# Update model
class DonationUpdate(BaseModel):
    status: str


# GET method - Home
@app.get("/")
def home():
    return {
        "message": "Welcome to MediShare API",
        "documentation": "/docs"
    }


# GET method - Health check
@app.get("/health")
def health():
    return {"status": "API is running"}


# POST method - Add donation
@app.post("/donations", status_code=201)
def add_donation(donation: Donation):

    if donation.expiry_date <= date.today():
        raise HTTPException(
            status_code=400,
            detail="Medicine expiry date must be in the future"
        )

    donation_id = str(uuid4())

    donation_data = donation.model_dump(mode="json")
    donation_data["id"] = donation_id
    donation_data["status"] = "Pending"

    donations[donation_id] = donation_data

    return {
        "message": "Donation submitted successfully",
        "donation": donation_data
    }


# GET method - View all donations
@app.get("/donations")
def get_donations():
    return {
        "total": len(donations),
        "donations": list(donations.values())
    }


# GET method - View one donation
@app.get("/donations/{donation_id}")
def get_donation(donation_id: str):

    if donation_id not in donations:
        raise HTTPException(
            status_code=404,
            detail="Donation not found"
        )

    return donations[donation_id]


# PUT method - Update donation status
@app.put("/donations/{donation_id}")
def update_donation(
    donation_id: str,
    update: DonationUpdate
):

    if donation_id not in donations:
        raise HTTPException(
            status_code=404,
            detail="Donation not found"
        )

    allowed_status = ["Pending", "Approved", "Rejected", "Collected"]

    if update.status not in allowed_status:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    donations[donation_id]["status"] = update.status

    return {
        "message": "Donation updated successfully",
        "donation": donations[donation_id]
    }


# DELETE method - Delete donation
@app.delete("/donations/{donation_id}")
def delete_donation(donation_id: str):

    if donation_id not in donations:
        raise HTTPException(
            status_code=404,
            detail="Donation not found"
        )

    deleted = donations.pop(donation_id)

    return {
        "message": "Donation deleted successfully",
        "donation": deleted
    }
