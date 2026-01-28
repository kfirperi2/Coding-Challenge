-- Table: public.model

-- DROP TABLE IF EXISTS public.model;

CREATE TABLE IF NOT EXISTS public.model
(
    id character(100) COLLATE pg_catalog."default" NOT NULL,
    name character(100) COLLATE pg_catalog."default" NOT NULL,
    "trim" character(100) COLLATE pg_catalog."default",
    manufacturer_id integer,
    horsepower integer,
    CONSTRAINT model_pkey PRIMARY KEY (id),
    CONSTRAINT unique_model_per_manufacturer UNIQUE (manufacturer_id, name, "trim"),
    CONSTRAINT fk_model_manufacturer FOREIGN KEY (manufacturer_id)
        REFERENCES public.manufacturer (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT,
    CONSTRAINT vehicle_horsepower_check CHECK (horsepower > 0)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.model
    OWNER to postgres;