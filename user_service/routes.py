from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import UserProfile
from utils import verify_jwt_token

router = APIRouter()

@router.post("/create")
def create_user(username: str, email: str, full_name: str, role: str, db: Session = Depends(get_db), token: dict = Depends(verify_jwt_token)):
    user = db.query(UserProfile).filter(UserProfile.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = UserProfile(username=username, email=email, full_name=full_name, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User profile created"}

@router.get("/profile")
def get_user_profile(username: str, db: Session = Depends(get_db), token: dict = Depends(verify_jwt_token)):
    user = db.query(UserProfile).filter(UserProfile.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
