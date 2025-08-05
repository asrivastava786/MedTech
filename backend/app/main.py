from fastapi import FastAPI
from db import prisma, connect_db, disconnect_db
from app.routes import auth  # if you've created routes/auth.py
from fastapi.middleware.cors import CORSMiddleware
from routes.medical import router as medical_router
from fastapi.staticfiles import StaticFiles
from routes import medical_record
from app.routes.medical import router as medical_router
from app.routes import medical_record


app = FastAPI()
app.include_router(auth.router)
app.include_router(medical_router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(medical_record.router, prefix="/api", tags=["Medical Records"])

@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

@app.get("/")
async def root():
    return {"message": "Hello, Medical Records Backend!"}

@app.get("/users")
async def get_users():
    users = await prisma.user.find_many()
    return users
