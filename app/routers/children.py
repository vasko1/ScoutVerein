from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models import Child, ChildStatus
from app.core.security import require_roles, get_current_user
from app.schemas import ChildCreate, ChildOut
from app.core.emailer import send_email

router = APIRouter(prefix="/children", tags=["children"])

@router.get("", response_model=List[ChildOut])
def list_children(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None),
    birth_year: Optional[int] = Query(None),
    status: Optional[ChildStatus] = Query(None),
):
    q = db.query(Child)
    if name:
        like = f"%{name}%"
        q = q.filter((Child.first_name.ilike(like)) | (Child.last_name.ilike(like)))
    if birth_year is not None:
        q = q.filter(Child.birth_year == birth_year)
    if status is not None:
        q = q.filter(Child.status == status)
    return q.order_by(Child.last_name.asc()).all()

@router.post("", response_model=ChildOut, dependencies=[Depends(require_roles("admin","scout"))])
def create_child(payload: ChildCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    child = Child(**payload.dict(), created_by_id=user.id)
    db.add(child); db.commit(); db.refresh(child)
    # Notify admin
    send_email(subject="Neues Kind angelegt", body=f"{child.first_name} {child.last_name} wurde von {user.name} angelegt.")
    return child

@router.get("/{child_id}", response_model=ChildOut)
def get_child(child_id: int, db: Session = Depends(get_db)):
    child = db.query(Child).get(child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return child