-- Table: public.vehicles

-- DROP TABLE IF EXISTS public.vehicles;

CREATE TABLE IF NOT EXISTS public.vehicles
(
    vin citext COLLATE pg_catalog."default" NOT NULL,
    manufacturer_name character(100) COLLATE pg_catalog."default",
    horse_power integer,
    model_name character(100) COLLATE pg_catalog."default",
    model_year integer,
    purchase_price numeric(12,2),
    fuel_type character(100) COLLATE pg_catalog."default",
    CONSTRAINT vehicles_pkey PRIMARY KEY (vin)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.vehicles
    OWNER to postgres;