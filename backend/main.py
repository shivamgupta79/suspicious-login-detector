# # # from fastapi import FastAPI
# # from fastapi import FastAPI

# # from routes import logins, alerts

# # app = FastAPI()

# # # Include routers
# # app.include_router(logins.router, prefix="/api")
# # app.include_router(alerts.router, prefix="/api")
# from fastapi import FastAPI
# from routes import logins, alerts

# app = FastAPI()

# app.include_router(logins.router, prefix="/api")
# app.include_router(alerts.router, prefix="/api")
from fastapi import FastAPI
from routes import logins, alerts  # routers import

app = FastAPI(title="Cyber Database API")  # optional: title add kiya

# Include routers
app.include_router(logins.router, prefix="/api/logins", tags=["Logins"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])

@app.get("/")
def root():
    return {"message": "API is running!"}
