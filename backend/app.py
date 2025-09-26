# # # from fastapi import FastAPI
# # # from pydantic import BaseModel
# # # from sqlalchemy.orm import Session
# # # from db.database import get_db, engine,Base
# # # from db.models import Base, User, Login, Alert

# # # app = FastAPI()
# # # Base.metadata.create_all(bind=engine)

# # # @app.get("/health")
# # # def health():
# # #     return {"ok":True}
# # # class LoginIn(BaseModel):
# # #     email: str
# # #     ip: str
# # #     city: str
# # #     device: str
# # #     status: str
# # #     ts: str | None = None

# # # def calc_score(level: str) -> float:
# # #     return {"green": 0.2, "yellow": 0.6, "red": 0.9}.get(level, 0.2)

# # # def detect_level(db: Session, user: User, login: Login) -> tuple[str,str]:
# # #     level, reasons = "green", []
# # #     if login.failed_count_window > 7: level, reasons = "red", ["failed_count>7"]
# # #     elif login.failed_count_window > 3: level, reasons = "yellow", ["failed_count>3"]
# # #     uc = set((user.usual_cities or "").split(","))
# # #     if login.city and login.city not in uc:
# # #         level = "yellow" if level == "green" else "red"
# # #         reasons.append("new_city")
# # #     return level, ", ".join(reasons) or "ok"

# # # @app.post("/logins")
# # # def post_logins(body: LoginIn, db: Session = Depends(get_db)):
# # #     user = db.query(User).filter(User.email == body.email).first()
# # #     if not user:
# # #         user = User(email=body.email, usual_cities=body.city or "", normal_hours="9-18")
# # #         db.add(user); db.commit(); db.refresh(user)
# # #     login = Login(user_id=user.id, ts=body.ts or "now", ip=body.ip, city=body.city,
# # #                   device=body.device, status=body.status,
# # #                   failed_count_window=(0 if body.status=="success" else 5))
# # #     db.add(login); db.commit(); db.refresh(login)
# # #     level, reason = detect_level(db, user, login)
# # #     if level in ("yellow","red"):
# # #         alert = Alert(user_id=user.id, ts=login.ts, reason=reason, level=level, score=calc_score(level))
# # #         db.add(alert); db.commit()
# # #     return {"ok": True, "level": level, "reason": reason}

# # # @app.get("/logins")
# # # def get_logins(db: Session = Depends(get_db)):
# # #     rows = db.query(Login).order_by(Login.ts.desc()).limit(50).all()
# # #     emails = {u.id: u.email for u in db.query(User).all()}
# # #     return [{"id":r.id,"email":emails.get(r.user_id,"?"),"ts":r.ts,"ip":r.ip,"city":r.city,"status":r.status,"failed":r.failed_count_window} for r in rows]

# # # @app.get("/alerts")
# # # def get_alerts(db: Session = Depends(get_db)):
# # #     rows = db.query(Alert).order_by(Alert.ts.desc()).limit(50).all()
# # #     return [{"id":r.id,"user_id":r.user_id,"ts":r.ts,"level":r.level,"score":r.score,"reason":r.reason} for r in rows]
# # from fastapi import FastAPI, Depends
# # from pydantic import BaseModel
# # from sqlalchemy.orm import Session
# # from db.database import get_db, engine, Base
# # from db.models import User, Login, Alert

# # # FastAPI app
# # app = FastAPI(title="Anuska DB + Alerts Module")

# # # Create tables
# # Base.metadata.create_all(bind=engine)

# # # Health check endpoint
# # @app.get("/health")
# # def health():
# #     return {"ok": True}

# # # Pydantic model for login input
# # class LoginIn(BaseModel):
# #     email: str
# #     ip: str
# #     city: str
# #     device: str
# #     status: str
# #     ts: str | None = None

# # # Score calculation
# # def calc_score(level: str) -> float:
# #     return {"green": 0.2, "yellow": 0.6, "red": 0.9}.get(level, 0.2)

# # # Level detection logic
# # def detect_level(db: Session, user: User, login: Login) -> tuple[str, str]:
# #     level, reasons = "green", []
# #     if login.failed_count_window > 7:
# #         level, reasons = "red", ["failed_count>7"]
# #     elif login.failed_count_window > 3:
# #         level, reasons = "yellow", ["failed_count>3"]

# #     uc = set((user.usual_cities or "").split(","))
# #     if login.city and login.city not in uc:
# #         level = "yellow" if level == "green" else "red"
# #         reasons.append("new_city")

# #     return level, ", ".join(reasons) or "ok"

# # # POST /logins endpoint
# # @app.post("/logins")
# # def post_logins(body: LoginIn, db: Session = Depends(get_db)):
# #     # Fetch or create user
# #     user = db.query(User).filter(User.email == body.email).first()
# #     if not user:
# #         user = User(
# #             email=body.email,
# #             usual_cities=body.city or "",
# #             normal_hours="9-18"
# #         )
# #         db.add(user)
# #         db.commit()
# #         db.refresh(user)

# #     # Create login record
# #     login = Login(
# #         user_id=user.id,
# #         ts=body.ts or "now",
# #         ip=body.ip,
# #         city=body.city,
# #         device=body.device,
# #         status=body.status,
# #         failed_count_window=(0 if body.status == "success" else 5)
# #     )
# #     db.add(login)
# #     db.commit()
# #     db.refresh(login)

# #     # Detect level and create alert if needed
# #     level, reason = detect_level(db, user, login)
# #     if level in ("yellow", "red"):
# #         alert = Alert(
# #             user_id=user.id,
# #             ts=login.ts,
# #             reason=reason,
# #             level=level,
# #             score=calc_score(level)
# #         )
# #         db.add(alert)
# #         db.commit()

# #     return {"ok": True, "level": level, "reason": reason}

# # # GET /logins endpoint
# # @app.get("/logins")
# # def get_logins(db: Session = Depends(get_db)):
# #     rows = db.query(Login).order_by(Login.ts.desc()).limit(50).all()
# #     emails = {u.id: u.email for u in db.query(User).all()}
# #     return [
# #         {
# #             "id": r.id,
# #             "email": emails.get(r.user_id, "?"),
# #             "ts": r.ts,
# #             "ip": r.ip,
# #             "city": r.city,
# #             "status": r.status,
# #             "failed": r.failed_count_window
# #         }
# #         for r in rows
# #     ]

# # # GET /alerts endpoint
# # @app.get("/alerts")
# # def get_alerts(db: Session = Depends(get_db)):
# #     rows = db.query(Alert).order_by(Alert.ts.desc()).limit(50).all()
# #     return [
# #         {
# #             "id": r.id,
# #             "user_id": r.user_id,
# #             "ts": r.ts,
# #             "level": r.level,
# #             "score": r.score,
# #             "reason": r.reason
# #         }
# #         for r in rows
# #     ]
# from fastapi import FastAPI
# from db.database import Base, engine
# from routes.logins import router as logins_router
# from routes.alerts import router as alerts_router

# app = FastAPI(title="Anuska DB + Alerts Module")

# # Create tables
# Base.metadata.create_all(bind=engine)

# # Health check
# @app.get("/health")
# def health():
#     return {"ok": True}

# # Include routers
# app.include_router(logins_router, prefix="/logins")
# app.include_router(alerts_router, prefix="/alerts")
from fastapi import FastAPI, Depends, WebSocket
from db.database import get_db, engine, Base

from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import get_db, engine, Base
from db.models import User, Login, Alert
from typing import List
import asyncio
import json

app = FastAPI(title="Anuska DB + Alerts Module")

# Create tables
Base.metadata.create_all(bind=engine)

# Health check
@app.get("/health")
def health():
    return {"ok": True}

# WebSocket connections list
ws_connections: List[WebSocket] = []

# WebSocket route for real-time alerts
@app.websocket("/ws/alerts")
async def websocket_alerts(ws: WebSocket):
    await ws.accept()
    ws_connections.append(ws)
    try:
        while True:
            await ws.receive_text()  # keep connection alive
    except:
        ws_connections.remove(ws)

# Function to broadcast alert to all connected clients
async def broadcast_alert(alert):
    data = {
        "user_id": alert.user_id,
        "level": alert.level,
        "reason": alert.reason,
        "score": alert.score,
        "ts": alert.ts
    }
    for conn in ws_connections:
        try:
            await conn.send_text(json.dumps(data))
        except:
            ws_connections.remove(conn)

# Pydantic model for login input
class LoginIn(BaseModel):
    email: str
    ip: str
    city: str
    device: str
    status: str
    ts: str | None = None

# Score calculation
def calc_score(level: str) -> float:
    return {"green": 0.2, "yellow": 0.6, "red": 0.9}.get(level, 0.2)

# Level detection logic
def detect_level(db: Session, user: User, login: Login) -> tuple[str, str]:
    level, reasons = "green", []
    if login.failed_count_window > 7:
        level, reasons = "red", ["failed_count>7"]
    elif login.failed_count_window > 3:
        level, reasons = "yellow", ["failed_count>3"]

    uc = set((user.usual_cities or "").split(","))
    if login.city and login.city not in uc:
        level = "yellow" if level == "green" else "red"
        reasons.append("new_city")

    return level, ", ".join(reasons) or "ok"

# POST /logins endpoint
@app.post("/logins")
def post_logins(body: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user:
        user = User(
            email=body.email,
            usual_cities=body.city or "",
            normal_hours="9-18"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    login = Login(
        user_id=user.id,
        ts=body.ts or "now",
        ip=body.ip,
        city=body.city,
        device=body.device,
        status=body.status,
        failed_count_window=(0 if body.status == "success" else 5)
    )
    db.add(login)
    db.commit()
    db.refresh(login)

    level, reason = detect_level(db, user, login)

    if level in ("yellow", "red"):
        alert = Alert(
            user_id=user.id,
            ts=login.ts,
            reason=reason,
            level=level,
            score=calc_score(level)
        )
        db.add(alert)
        db.commit()
        # Broadcast alert to WebSocket clients
        asyncio.create_task(broadcast_alert(alert))

    return {"ok": True, "level": level, "reason": reason}

# GET /logins endpoint
@app.get("/logins")
def get_logins(db: Session = Depends(get_db)):
    rows = db.query(Login).order_by(Login.ts.desc()).limit(50).all()
    emails = {u.id: u.email for u in db.query(User).all()}
    return [
        {
            "id": r.id,
            "email": emails.get(r.user_id, "?"),
            "ts": r.ts,
            "ip": r.ip,
            "city": r.city,
            "status": r.status,
            "failed": r.failed_count_window
        }
        for r in rows
    ]

# GET /alerts endpoint
@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    rows = db.query(Alert).order_by(Alert.ts.desc()).limit(50).all()
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "ts": r.ts,
            "level": r.level,
            "score": r.score,
            "reason": r.reason
        }
        for r in rows
    ]
