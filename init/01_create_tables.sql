CREATE TABLE IF NOT EXISTS public.energy_readings
(
    id           SERIAL PRIMARY KEY,
    meter_id     varchar          NOT NULL,
    "timestamp"  timestamptz      NOT NULL,
    kwh          double precision NOT NULL,
    reading_type varchar          NOT NULL,
    CONSTRAINT uq_reading_meter_ts_type
        UNIQUE (meter_id, "timestamp", reading_type),
    CONSTRAINT energy_readings_kwh_check
        CHECK (kwh >= 0),
    CONSTRAINT energy_readings_reading_type_check
        CHECK (reading_type IN ('consumption', 'generation'))
);

CREATE INDEX IF NOT EXISTS ix_energy_readings_meter_id_timestamp
    ON public.energy_readings (meter_id, "timestamp");