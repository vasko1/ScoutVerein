from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models import Report, Child
from app.core.security import require_roles, get_current_user
from app.schemas import ReportCreate, ReportOut
from app.core.emailer import send_email

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("", response_model=ReportOut, dependencies=[Depends(require_roles("admin","scout"))])
def create_report(payload: ReportCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    child = db.query(Child).get(payload.child_id)
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    report = Report(child_id=payload.child_id, author_id=user.id, text=payload.text)
    db.add(report); db.commit(); db.refresh(report)
    send_email(subject="Neuer Bericht erstellt", body=f"Bericht zu Kind-ID {payload.child_id} von {user.name}.")
    return report

@router.get("/child/{child_id}", response_model=List[ReportOut])
def list_reports_for_child(child_id: int, db: Session = Depends(get_db)):
    return db.query(Report).filter(Report.child_id == child_id).order_by(Report.created_at.desc()).all()