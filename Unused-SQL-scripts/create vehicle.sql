-- Table: public.vehicle

DROP TABLE IF EXISTS public.vehicle;

CREATE TABLE IF NOT EXISTS public.vehicle
(
    vin citext COLLATE pg_catalog."default" NOT NULL,
    model_id character(100),
    fuel_id integer,
    model_year integer NOT NULL,
    purchase_price numeric(12,2),
    description text COLLATE pg_catalog."default",
    last_updated timestamp without time zone DEFAULT now(),
    CONSTRAINT vehicle_pkey PRIMARY KEY (vin),
    CONSTRAINT vehicle_vin_check CHECK (length(vin::text) = 17),
	
	CONSTRAINT fk_vehicle_model
        FOREIGN KEY (model_id)
        REFERENCES model(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_vehicle_fuel
        FOREIGN KEY (fuel_id)
        REFERENCES fuel(id)
        ON DELETE RESTRICT
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.vehicle
    OWNER to postgres;