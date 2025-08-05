from fastapi import UploadFile
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# --------------------
# MedicalRecord Schemas
# --------------------

class MedicalRecordBase(BaseModel):
    recordType: str
    conditionName: str
    category: str
    ageOfOnset: Optional[int]
    severity: Optional[str]
    isGenetic: bool = False
    treatmentNotes: Optional[str]
    diagnosedAt: Optional[datetime]


class MedicalRecordCreate(MedicalRecordBase):
    userId: Optional[str]
    familyMemberId: Optional[str]


class MedicalRecordResponse(MedicalRecordBase):
    id: str
    userId: Optional[str]
    familyMemberId: Optional[str]
    recordedById: str
    createdAt: datetime
    updatedAt: datetime  # 

    class Config:
        orm_mode = True

class MedicalRecordCreate(MedicalRecordBase):
    userId: Optional[str]
    familyMemberId: Optional[str]
    recordedById: Optional[str]  # <-- only if you allow this to be passed, otherwise derive from token

class MedicalRecordUpdate(BaseModel):
    recordType: Optional[str]
    conditionName: Optional[str]
    category: Optional[str]
    ageOfOnset: Optional[int]
    severity: Optional[str]
    isGenetic: Optional[bool]
    treatmentNotes: Optional[str]
    diagnosedAt: Optional[datetime]

# --------------------
# Symptom Schemas
# --------------------

class SymptomBase(BaseModel):
    symptom: str
    severity: Optional[str]
    onsetDate: Optional[datetime]
    durationDays: Optional[int]
    associatedCondition: Optional[str]


class SymptomCreate(SymptomBase):
    userId: Optional[str]
    familyMemberId: Optional[str]


class SymptomResponse(SymptomBase):
    id: str
    userId: Optional[str]
    familyMemberId: Optional[str]
    addedById: str
    createdAt: datetime

    class Config:
        orm_mode = True


# --------------------
# MedicalAsset Schemas
# --------------------

class MedicalAssetBase(BaseModel):
    category: Optional[str]
    tags: Optional[List[str]]
    associatedRecordId: Optional[str]
    familyMemberId: Optional[str]
    groupId: Optional[str]


class MedicalAssetCreate(MedicalAssetBase):
    userId: str
    file: UploadFile
    familyMemberId: Optional[str]   


class MedicalAssetResponse(MedicalAssetBase):
    id: str
    userId: str
    familyMemberId: Optional[str]
    createdAt: datetime
    uploadedById: str
    fileName: str
    filePath: str

    class Config:
        orm_mode = True


# --------------------
# RiskFactor Schemas
# --------------------

class RiskFactorBase(BaseModel):
    bmi: Optional[float]
    smokingStatus: Optional[str]
    alcoholUse: Optional[str]
    physicalActivity: Optional[str]
    dietType: Optional[str]
    occupationType: Optional[str]
    stressLevel: Optional[str]


class RiskFactorCreate(RiskFactorBase):
    userId: Optional[str]
    familyMemberId: Optional[str]


class RiskFactorResponse(RiskFactorBase):
    id: str
    userId: Optional[str]
    familyMemberId: Optional[str]
    createdAt: datetime

    class Config:
        orm_mode = True


# ----------------------------
# EnvironmentalFactor Schemas
# ----------------------------

class EnvironmentalFactorBase(BaseModel):
    location: Optional[str]
    pollutionLevel: Optional[str]
    diseaseOutbreaks: Optional[str]


class EnvironmentalFactorCreate(EnvironmentalFactorBase):
    userId: Optional[str]
    familyMemberId: Optional[str]


class EnvironmentalFactorResponse(EnvironmentalFactorBase):
    id: str
    userId: Optional[str]
    familyMemberId: Optional[str]
    createdAt: datetime

    class Config:
        orm_mode = True

#extra schemas can be added here as needed
# Already included in your last message, so assuming present:
class RiskFactorCreate(BaseModel):
    name: str
    description: Optional[str] = None
    userId: Optional[str] = None
    familyMemberId: Optional[str] = None

class RiskFactorResponse(RiskFactorCreate):
    id: str

class EnvironmentalFactorCreate(BaseModel):
    name: str
    description: Optional[str] = None
    userId: Optional[str] = None
    familyMemberId: Optional[str] = None

class EnvironmentalFactorResponse(EnvironmentalFactorCreate):
    id: str
