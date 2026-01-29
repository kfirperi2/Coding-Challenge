-- Table: public.fuel

-- DROP TABLE IF EXISTS public.fuel;

CREATE TABLE IF NOT EXISTS public.fuel
(
    id integer NOT NULL,
    type character(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT fuel_pkey PRIMARY KEY (id),
    CONSTRAINT fuel_type_key UNIQUE (type)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.fuel
    OWNER to postgres;