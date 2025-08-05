from fastapi import APIRouter, Depends, HTTPException
from prisma import Prisma
from app.dependencies import get_db, get_current_user
from app import schemas
from typing import List, Optional

router = APIRouter()

@router.post("/symptoms", response_model=schemas.SymptomResponse)
async def create_symptom(
    symptom: schemas.SymptomCreate,
    db: Prisma = Depends(get_db),
    user=Depends(get_current_user),
):
    created = await db.symptom.create(
        data={
            **symptom.dict(exclude_unset=True),
            "addedById": user.id,
        }
    )
    return created


@router.get("/symptoms", response_model=List[schemas.SymptomResponse])
async def get_symptoms(
    userId: Optional[str] = None,
    familyMemberId: Optional[str] = None,
    db: Prisma = Depends(get_db),
    user=Depends(get_current_user),
):
    filters = {}
    if userId:
        filters["userId"] = userId
    if familyMemberId:
        filters["familyMemberId"] = familyMemberId

    return await db.symptom.find_many(where=filters)


@router.patch("/symptoms/{symptom_id}", response_model=schemas.SymptomResponse)
async def update_symptom(
    symptom_id: str,
    update: schemas.SymptomUpdate,
    db: Prisma = Depends(get_db),
    user=Depends(get_current_user),
):
    existing = await db.symptom.find_unique(where={"id": symptom_id})
    if not existing:
        raise HTTPException(404, "Symptom not found")

    return await db.symptom.update(
        where={"id": symptom_id}, data=update.dict(exclude_unset=True)
    )


@router.delete("/symptoms/{symptom_id}")
async def delete_symptom(
    symptom_id: str,
    db: Prisma = Depends(get_db),
    user=Depends(get_current_user),
):
    existing = await db.symptom.find_unique(where={"id": symptom_id})
    if not existing:
        raise HTTPException(404, "Symptom not found")

    await db.symptom.delete(where={"id": symptom_id})
    return {"detail": "Deleted"}