from fastapi import FastAPI
from app.energy_readings.queries.list_readings.router import router as list_readings_router
from app.energy_readings.queries.get_reading_by_id.router  import router as get_reading_by_id_router
from app.energy_readings.queries.get_daily_aggregates.router  import router as daily_aggregates_router
from app.energy_readings.commands.create_reading.router  import router as create_reading_router
from app.energy_readings.commands.bulk_import_readings.router import router as bulk_import_readings_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(daily_aggregates_router)
app.include_router(get_reading_by_id_router)
app.include_router(list_readings_router)
app.include_router(bulk_import_readings_router)
app.include_router(create_reading_router)


