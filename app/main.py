from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base, SessionLocal
from app.core import models
from app.core.seed import seed
from app.routers import auth as auth_router
from app.routers import children as children_router
from app.routers import reports as reports_router
from app.routers import events as events_router
from app.routers import users as users_router

Base.metadata.create_all(bind=engine)

def init_seed():
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()

app = FastAPI(title="ScoutVerein API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_seed()

app.include_router(auth_router.router)
app.include_router(children_router.router)
app.include_router(reports_router.router)
app.include_router(events_router.router)
app.include_router(users_router.router)

@app.get("/health")
def health():
    return {"status": "ok"}