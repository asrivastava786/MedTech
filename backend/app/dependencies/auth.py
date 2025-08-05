from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from auth import SECRET_KEY, ALGORITHM
from db import prisma
from fastapi import HTTPException, Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await prisma.user.find_unique(where={"email": email})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

async def get_current_doctor(user=Depends(get_current_user)):
    if user.role != "DOCTOR":
        raise HTTPException(status_code=403, detail="Doctor access required")
    return user

async def get_current_admin(user=Depends(get_current_user)):
    if user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user