CREATE TABLE IF NOT EXISTS public.energy_reading
(
    id SERIAL PRIMARY KEY,
    meter_id character varying NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    age double precision,
    reading_type character varying NOT NULL,
    CONSTRAINT energy_reading_reading_type_check
        CHECK (reading_type IN ('consumption', 'generation'))
);

