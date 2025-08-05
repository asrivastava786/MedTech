from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from db import prisma
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter()

class SignupRequest(BaseModel):
    email: str
    name: str
    password: str

@router.post("/signup")
async def signup(user: SignupRequest):
    existing = await prisma.user.find_unique(where={"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed = hash_password(user.password)
    await prisma.user.create(data={
        "email": user.email,
        "name": user.name,
        "password": hashed

    })
    return {"message": "Signup successful"}

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(data: LoginRequest):
    user = await prisma.user.find_unique(where={"email": data.email},select={"id": True, "email": True, "name": True, "password": True, "role": True})
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": user.email, "role": user.role, "id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": {"email": user.email, "name": user.name, "role": user.role}}
