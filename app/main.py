from fastapi import FastAPI 
import uvicorn
from routes import user, hive, bee_type, analysis_backup, hive_analysis, access, company, sensor, auth
from db.database import Base, engine
from core.middleware import ActiveUserMiddleware
from seed import seed_data

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(ActiveUserMiddleware)

app.include_router(company.router)
app.include_router(user.router)
app.include_router(hive.router)
app.include_router(access.router)
app.include_router(bee_type.router)
app.include_router(analysis_backup.router)
app.include_router(hive_analysis.router)
app.include_router(sensor.router)
app.include_router(auth.router)

@app.on_event("startup")
def startup_event():
    seed_data()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)