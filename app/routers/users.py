from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, hash_password
from app.schemas import UserOut, UserUpdatePassword

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user

@router.post("/me/password")
def change_password(payload: UserUpdatePassword, db: Session = Depends(get_db), user=Depends(get_current_user)):
    user.password_hash = hash_password(payload.new_password)
    db.add(user); db.commit()
    return {"ok": True}