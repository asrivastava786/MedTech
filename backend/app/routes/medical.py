from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from prisma.models import (
    MedicalRecord,
    Symptom,
    MedicalAsset,
    RiskFactor,
    EnvironmentalFactor
)
from prisma import Prisma
from schemas import medical as schemas
from dependencies.auth import get_current_user

router = APIRouter(prefix="/medical", tags=["Medical"])

# Dependency to get DB client
async def get_db() -> Prisma:
    db = Prisma()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()


@router.post("/records/", response_model=schemas.MedicalRecordResponse)
async def create_medical_record(record: schemas.MedicalRecordCreate, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    db_record = await db.medicalrecord.create(
        data={
            **record.dict(exclude_unset=True),
            "recordedById": user.id,
        }
    )
    return db_record


@router.get("/records/{record_id}", response_model=schemas.MedicalRecordResponse)
async def get_medical_record(record_id: str, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    record = await db.medicalrecord.find_unique(where={"id": record_id})
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record


@router.delete("/records/{record_id}")
async def delete_medical_record(record_id: str, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    await db.medicalrecord.delete(where={"id": record_id})
    return {"message": "Medical record deleted"}

@router.post("/symptoms/", response_model=schemas.SymptomResponse)
async def add_symptom(symptom: schemas.SymptomCreate, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    db_symptom = await db.symptom.create(
        data={
            **symptom.dict(exclude_unset=True),
            "addedById": user.id
        }
    )
    return db_symptom


@router.get("/symptoms/{symptom_id}", response_model=schemas.SymptomResponse)
async def get_symptom(symptom_id: str, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    symptom = await db.symptom.find_unique(where={"id": symptom_id})
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return symptom


@router.delete("/symptoms/{symptom_id}")
async def delete_symptom(symptom_id: str, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    await db.symptom.delete(where={"id": symptom_id})
    return {"message": "Symptom deleted"}

@router.post("/assets/", response_model=schemas.MedicalAssetResponse)
async def upload_medical_asset(asset: schemas.MedicalAssetCreate, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    db_asset = await db.medicalasset.create(data=asset.dict())
    return db_asset

@router.post("/risk-factors/", response_model=schemas.RiskFactorResponse)
async def create_risk_factor(data: schemas.RiskFactorCreate, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    db_rf = await db.riskfactor.create(data=data.dict())
    return db_rf

@router.post("/environmental-factors/", response_model=schemas.EnvironmentalFactorResponse)
async def create_environmental(data: schemas.EnvironmentalFactorCreate, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    db_env = await db.environmentalfactor.create(data=data.dict())
    return db_env


#extra endpoints for risk factors and environmental factors can be added similarly

@router.post("/risk-factors/", response_model=schemas.RiskFactorResponse)
async def add_risk_factor(factor: schemas.RiskFactorCreate, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    db_factor = await db.riskfactor.create(data=factor.dict())
    return db_factor

@router.get("/risk-factors/{factor_id}", response_model=schemas.RiskFactorResponse)
async def get_risk_factor(factor_id: str, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    factor = await db.riskfactor.find_unique(where={"id": factor_id})
    if not factor:
        raise HTTPException(status_code=404, detail="Risk factor not found")
    return factor

@router.delete("/risk-factors/{factor_id}")
async def delete_risk_factor(factor_id: str, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    await db.riskfactor.delete(where={"id": factor_id})
    return {"message": "Risk factor deleted"}


@router.post("/environmental-factors/", response_model=schemas.EnvironmentalFactorResponse)
async def add_environmental_factor(factor: schemas.EnvironmentalFactorCreate, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    db_factor = await db.environmentalfactor.create(data=factor.dict())
    return db_factor

@router.get("/environmental-factors/{factor_id}", response_model=schemas.EnvironmentalFactorResponse)
async def get_environmental_factor(factor_id: str, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    factor = await db.environmentalfactor.find_unique(where={"id": factor_id})
    if not factor:
        raise HTTPException(status_code=404, detail="Environmental factor not found")
    return factor

@router.delete("/environmental-factors/{factor_id}")
async def delete_environmental_factor(factor_id: str, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    await db.environmentalfactor.delete(where={"id": factor_id})
    return {"message": "Environmental factor deleted"}

@router.patch("/records/{record_id}", response_model=schemas.MedicalRecordResponse)
async def update_medical_record(record_id: str, update: schemas.MedicalRecordCreate, db: Prisma = Depends(get_db)):
    return await db.medicalrecord.update(
        where={"id": record_id},
        data=update.dict(exclude_unset=True)
    )

#patch endpoints for symptoms, assets, risk factors, and environmental factors can be added similarly

@router.patch("/medical-records/{record_id}", response_model=schemas.MedicalRecordResponse)
async def update_medical_record(record_id: str, update: schemas.MedicalRecordUpdate, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    existing = await db.medicalrecord.find_unique(where={"id": record_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Medical record not found")

    # Only allow owner or admin (optional: use role-based access control)
    if existing.userId and existing.userId != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to modify this record")

    updated = await db.medicalrecord.update(
        where={"id": record_id},
        data=update.dict(exclude_unset=True)
    )
    return updated

@router.patch("/symptoms/{symptom_id}", response_model=schemas.SymptomResponse)
async def update_symptom(symptom_id: str, update: schemas.SymptomCreate, db: Prisma = Depends(get_db)):
    return await db.symptom.update(
        where={"id": symptom_id},
        data=update.dict(exclude_unset=True)
    )

@router.patch("/medical-assets/{asset_id}", response_model=schemas.MedicalAssetResponse)
async def update_medical_asset(asset_id: str, update: schemas.MedicalAssetCreate, db: Prisma = Depends(get_db)):
    return await db.medicalasset.update(
        where={"id": asset_id},
        data=update.dict(exclude_unset=True)
    )

@router.patch("/risk-factors/{factor_id}", response_model=schemas.RiskFactorResponse)
async def update_risk_factor(factor_id: str, update: schemas.RiskFactorCreate, db: Prisma = Depends(get_db)):
    return await db.riskfactor.update(
        where={"id": factor_id},
        data=update.dict(exclude_unset=True)
    )

@router.patch("/environmental-factors/{factor_id}", response_model=schemas.EnvironmentalFactorResponse)
async def update_environmental_factor(factor_id: str, update: schemas.EnvironmentalFactorCreate, db: Prisma = Depends(get_db)):
    return await db.environmentalfactor.update(
        where={"id": factor_id},
        data=update.dict(exclude_unset=True)
    )
