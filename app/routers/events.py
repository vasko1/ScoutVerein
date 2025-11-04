from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models import Event, Attendance
from app.core.security import require_roles, get_current_user
from app.schemas import EventCreate, EventOut
from app.core.emailer import send_email

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", response_model=List[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.date.asc()).all()

@router.post("", response_model=EventOut, dependencies=[Depends(require_roles("admin"))])
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    ev = Event(**payload.dict())
    db.add(ev); db.commit(); db.refresh(ev)
    return ev

@router.post("/{event_id}/attend", dependencies=[Depends(require_roles("admin","scout"))])
def attend_event(event_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ev = db.query(Event).get(event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    existing = db.query(Attendance).filter(Attendance.event_id==event_id, Attendance.user_id==user.id).first()
    if not existing:
        existing = Attendance(event_id=event_id, user_id=user.id, status="zugesagt")
        db.add(existing); db.commit()
        send_email(subject="Event-Zusage", body=f"{user.name} hat für '{ev.title}' zugesagt.")
    return {"ok": True}