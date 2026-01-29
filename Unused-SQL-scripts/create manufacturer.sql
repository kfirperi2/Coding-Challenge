-- Table: public.manufacturer

-- DROP TABLE IF EXISTS public.manufacturer;

CREATE TABLE IF NOT EXISTS public.manufacturer
(
    id integer NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    country text COLLATE pg_catalog."default",
    factory_location character(100) COLLATE pg_catalog."default",
    CONSTRAINT manufacturer_pkey PRIMARY KEY (id),
    CONSTRAINT manufacturer_name_key UNIQUE (name, factory_location)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.manufacturer
    OWNER to postgres;