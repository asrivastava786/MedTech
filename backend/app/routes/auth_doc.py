from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_doctor, get_current_admin

from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserResponse
from auth import hash_password
from token import create_access_token
from db import get_db
from prisma import Prisma
from app.schemas import User
import re

router = APIRouter()

@router.get("/doctor-panel")
async def doctor_only_route(doctor=Depends(get_current_doctor)):
    return {"message": f"Welcome Doctor {doctor.name}"}

@router.get("/admin-dashboard")
async def admin_only_route(admin=Depends(get_current_admin)):
    return {"message": "Welcome Admin"}

# Optional: fake license validator (can later replace with API call)
def is_valid_license_number(license_number: str) -> bool:
    # Just a placeholder check (e.g., must be alphanumeric and 6-12 chars)
    return bool(re.fullmatch(r"[A-Z0-9]{6,12}", license_number))


@router.post("/auth/doctor-signup", response_model=UserResponse)
async def doctor_signup(data: UserCreate, db: Prisma = Depends(get_db)):
    if data.role != "DOCTOR":
        raise HTTPException(status_code=400, detail="This route is for doctors only.")

    if not data.licenseNumber:
        raise HTTPException(status_code=400, detail="License number is required for doctors.")

    if not is_valid_license_number(data.licenseNumber):
        raise HTTPException(status_code=400, detail="Invalid license number format.")

    existing_user = await db.user.find_unique(where={"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await db.user.create(
        data={
            "email": data.email,
            "hashedPassword": hash_password(data.password),
            "fullName": data.fullName,
            "role": "DOCTOR",
            "licenseNumber": data.licenseNumber
        }
    )

    return user