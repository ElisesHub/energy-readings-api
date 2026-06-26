from datetime import datetime
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.energy_readings.shared.energy_reading import EnergyReading
from app.energy_readings.shared.energy_reading_type import EnergyReadingType

def test_get_reading_by_id_ok(http_client: TestClient, db_session: Session):

        # Arrange — insert a known reading so the test owns its own data
        test_meter_id = "TST-007-35173000"
        reading = EnergyReading(
            meter_id=test_meter_id,
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
            kwh=42.5,
            reading_type=EnergyReadingType.GENERATION,
        )
        db_session.add(reading)
        db_session.commit()
        db_session.refresh(reading)  # populates reading.id with the DB-assigned value

        # Act
        response = http_client.get(f"/readings/{reading.id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["meter_id"] == test_meter_id
        assert data["timestamp"] == "2026-01-01T12:00:00Z"
        assert data["kwh"] == 42.5
        assert data["reading_type"] == EnergyReadingType.GENERATION.value
