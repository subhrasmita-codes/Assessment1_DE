CREATE TABLE IF NOT EXISTS raw.weather_daily (
    date DATE NOT NULL,
    city TEXT NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    temperature_2m_max DOUBLE PRECISION,
    temperature_2m_min DOUBLE PRECISION,
    precipitation_sum DOUBLE PRECISION,
    PRIMARY KEY (date, city)
);