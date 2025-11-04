from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from app.core.models import User, RoleEnum, Child, ChildStatus, Report, Event
from app.core.security import hash_password
from app.core.settings import settings
from app.core.emailer import send_email

def seed(db: Session):
    # Admin anlegen (falls nicht vorhanden)
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if not admin:
        admin = User(
            name="Admin",
            email=settings.ADMIN_EMAIL,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role=RoleEnum.admin,
        )
        db.add(admin)
        db.commit()
        print(">> Admin angelegt:", settings.ADMIN_EMAIL)

    # Beispiel-Nutzer
    if not db.query(User).filter(User.email == "scout1@verein.de").first():
        scout1 = User(name="Scout Eins", email="scout1@verein.de", password_hash=hash_password("pass123"), role=RoleEnum.scout)
        scout2 = User(name="Scout Zwei", email="scout2@verein.de", password_hash=hash_password("pass123"), role=RoleEnum.scout)
        praktikant = User(name="Praktikant Paul", email="praktikant@verein.de", password_hash=hash_password("pass123"), role=RoleEnum.praktikant)
        db.add_all([scout1, scout2, praktikant])
        db.commit()
        print(">> Beispielnutzer angelegt")

    scout = db.query(User).filter(User.email=="scout1@verein.de").first()
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()

    # Kinder
    if db.query(Child).count() == 0:
        c1 = Child(first_name="Mia", last_name="Schmidt", birth_date=date(2014,5,12), birth_year=2014, parent_name="Frau Schmidt", phone="01234", status=ChildStatus.aktiv, created_by_id=scout.id if scout else None)
        c2 = Child(first_name="Leo", last_name="Müller", birth_date=date(2013,8,30), birth_year=2013, parent_name="Herr Müller", phone="05678", status=ChildStatus.weiter_beobachten, created_by_id=scout.id if scout else None)
        c3 = Child(first_name="Sofia", last_name="Klein", birth_date=date(2015,2,20), birth_year=2015, parent_name="Frau Klein", phone="09876", status=ChildStatus.aktiv, created_by_id=scout.id if scout else None)
        db.add_all([c1,c2,c3]); db.commit()
        print(">> Kinder angelegt")

        # Berichte
        r1 = Report(child_id=c1.id, author_id=scout.id if scout else admin.id, text="Erstkontakt beim Probetraining. Sehr motiviert.", created_at=datetime.utcnow())
        r2 = Report(child_id=c2.id, author_id=scout.id if scout else admin.id, text="Weiter beobachten: Kondition gut, soziale Integration prüfen.", created_at=datetime.utcnow())
        db.add_all([r1, r2]); db.commit()
        print(">> Berichte angelegt")

        send_email(subject="Neues Kind angelegt", body=f"Mia Schmidt wurde angelegt von {scout.name if scout else 'System'}.")
        send_email(subject="Neuer Bericht erstellt", body=f"Bericht für Leo Müller von {scout.name if scout else 'System'}.")

    # Event
    if db.query(Event).count() == 0:
        ev = Event(title="Scouting Probetraining", address="Sportplatz Hauptstraße 1", date=datetime.utcnow()+timedelta(days=7), link="https://maps.example.com", description="Sichtung und Probetraining")
        db.add(ev); db.commit()
        print(">> Event angelegt")