-- Crear el usuario si no existe

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'weather') THEN
        CREATE ROLE weather WITH LOGIN PASSWORD 'weather_pass';
    END IF;
END $$;


DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'weatherdb') THEN
        CREATE DATABASE weatherdb OWNER weather;
    END IF;
END $$;


\connect weatherdb

CREATE TABLE IF NOT EXISTS weather_logs (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(50),
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
