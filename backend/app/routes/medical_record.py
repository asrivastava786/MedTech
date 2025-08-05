from fastapi import APIRouter, Depends, HTTPException
from prisma import Prisma
from prisma.models import MedicalRecord
from app.dependencies import get_db, get_current_user
from app import schemas
from typing import List, Optional

router = APIRouter()


@router.post("/medical-records", response_model=schemas.MedicalRecordResponse)
async def create_medical_record(
    record: schemas.MedicalRecordCreate,
    db: Prisma = Depends(get_db),
    user=Depends(get_current_user),
):
    created = await db.medicalrecord.create(
        data={
            **record.dict(exclude_unset=True),
            "recordedById": user.id,
        }
    )
    return created


@router.get("/medical-records", response_model=List[schemas.MedicalRecordResponse])
async def get_all_medical_records(
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

    records = await db.medicalrecord.find_many(
        where=filters,
        order={"createdAt": "desc"},
    )
    return records


@router.get("/medical-records/{record_id}", response_model=schemas.MedicalRecordResponse)
async def get_medical_record_by_id(
    record_id: str,
    db: Prisma = Depends(get_db),
    user=Depends(get_current_user),
):
    record = await db.medicalrecord.find_unique(where={"id": record_id})
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record


@router.patch("/medical-records/{record_id}", response_model=schemas.MedicalRecordResponse)
async def update_medical_record(
    record_id: str,
    update: schemas.MedicalRecordUpdate,
    db: Prisma = Depends(get_db),
    user=Depends(get_current_user),
):
    record = await db.medicalrecord.find_unique(where={"id": record_id})
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    updated = await db.medicalrecord.update(
        where={"id": record_id},
        data=update.dict(exclude_unset=True),
    )
    return updated


@router.delete("/medical-records/{record_id}")
async def delete_medical_record(
    record_id: str,
    db: Prisma = Depends(get_db),
    user=Depends(get_current_user),
):
    record = await db.medicalrecord.find_unique(where={"id": record_id})
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    await db.medicalrecord.delete(where={"id": record_id})
    return {"detail": "Deleted successfully"}
