from ast import List
import os
from typing import Optional
import uuid
import shutil
from fastapi.responses import FileResponse
import magic
import clamd

from fastapi import UploadFile, File, Form, APIRouter, Depends, HTTPException
from app.schemas.medical import MedicalAssetResponse
from prisma import Prisma
from app import get_db
from app.auth import get_current_user

router = APIRouter()
UPLOAD_FOLDER = "uploads"
ALLOWED_MIME_TYPES = ["application/pdf", "image/png", "image/jpeg"]

clamd_client = clamd.ClamdUnixSocket()  # For Linux/macOS
# clamd_client = clamd.ClamdNetworkSocket(host='127.0.0.1', port=3310)  # If using TCP

@router.post("/medical-assets/upload")
async def upload_medical_asset(
    file: UploadFile = File(...),
    name: str = Form(...),
    type: str = Form(...),
    tags: Optional[str] = Form(None), 
    category: Optional[str] = Form(None),
    associatedRecordId: str = Form(None),
    familyMemberId: str = Form(None),
    groupId: Optional[str] = Form(None),
    db: Prisma = Depends(get_db),
    user=Depends(get_current_user)
):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Read file bytes
    contents = await file.read()

    # 🔐 MIME Type Detection
    mime_type = magic.from_buffer(contents, mime=True)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid file type: {mime_type}")

    # 🛡️ Antivirus Scan
    result = clamd_client.instream(contents)
    if result.get("stream", [None, ""])[0] == "FOUND":
        raise HTTPException(status_code=400, detail="Virus detected in file upload.")

    # Save file
    ext = os.path.splitext(file.filename)[1]
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}{ext}")
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    url = f"/{file_path}"
    tag_list = [t.strip() for t in tags.split(",")] if tags else []

    # Save metadata to DB
    asset = await db.medicalasset.create({
        "name": name,
        "type": type,
        "url": url,
        "associatedRecordId": associatedRecordId,
        "familyMemberId": familyMemberId,
        "userId": user["id"],
        "tags": tag_list,
        "category": category,
        "uploadedById": user.id,
        "groupId": groupId
    })

    return asset

@router.get("/medical-assets/{asset_id}/download")
async def download_asset(asset_id: str, db: Prisma = Depends(get_db)):
    asset = await db.medicalasset.find_unique(where={"id": asset_id})
    if not asset or not os.path.exists(asset.filePath):
        raise HTTPException(404, "File not found")
    return FileResponse(asset.filePath, filename=asset.fileName)


@router.delete("/medical-assets/{asset_id}")
async def delete_asset(asset_id: str, db: Prisma = Depends(get_db)):
    asset = await db.medicalasset.find_unique(where={"id": asset_id})
    if not asset:
        raise HTTPException(404, "Asset not found")
    if os.path.exists(asset.filePath):
        os.remove(asset.filePath)
    await db.medicalasset.delete(where={"id": asset_id})
    return {"detail": "Deleted"}


@router.get("/groups/{group_id}", response_model=List[MedicalAssetResponse])
async def get_assets_by_group(group_id: str, db: Prisma = Depends(get_db), user=Depends(get_current_user)):
    assets = await db.medicalasset.find_many(where={"groupId": group_id})
    return assets
