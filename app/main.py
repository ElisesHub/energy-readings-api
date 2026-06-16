
from fastapi import FastAPI
from app.energy_readings.queries.get_data_reports.routers import router as get_data_reports_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(get_data_reports_router)
