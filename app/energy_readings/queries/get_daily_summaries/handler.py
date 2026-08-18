from sqlalchemy.sql.functions import func
from sqlmodel import Session, select
from app.energy_readings.shared.energy_reading import EnergyReading
from app.energy_readings.shared.energy_reading_type import EnergyReadingType
from .schemas import DailySummaryParams



def handle(session: Session, params: DailySummaryParams):

    day = func.date_trunc("day", EnergyReading.timestamp).label("day")

    consumed = func.coalesce(func.sum(EnergyReading.kwh).filter(EnergyReading.reading_type == EnergyReadingType.CONSUMPTION), 0)
    generated = func.coalesce(func.sum(EnergyReading.kwh).filter(EnergyReading.reading_type == EnergyReadingType.GENERATION), 0)

    query = select(day,
                   func.count(EnergyReading.id).label("reading_count"),
                   consumed.label("kwh_consumed"),
                   generated.label("kwh_generated"),
                   (consumed - generated).label("kwh_net_import"))

    query = query.where(

        EnergyReading.meter_id == params.meter_id,
        EnergyReading.timestamp >= params.date_from,
        EnergyReading.timestamp < params.date_to)

    query = query.group_by(day)
    query = query.order_by(day)

    result = session.exec(query).all()

    return result
