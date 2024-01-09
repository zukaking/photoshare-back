-- Table: public.user_info

-- DROP TABLE IF EXISTS public.user_info;

CREATE TABLE IF NOT EXISTS public.user_info
(
    user_id smallserial NOT NULL ,
    email text COLLATE pg_catalog."default",
    password text COLLATE pg_catalog."default",
    username text COLLATE pg_catalog."default",
    CONSTRAINT user_info_pkey PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_info
    OWNER to postgres;


-- Table: public.album_info

-- DROP TABLE IF EXISTS public.album_info;

CREATE TABLE IF NOT EXISTS public.album_info
(
    album_id smallserial NOT NULL,
    CONSTRAINT album_info_pkey PRIMARY KEY (album_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.album_info
    OWNER to postgres;


-- Table: public.file_info

-- DROP TABLE IF EXISTS public.file_info;

CREATE TABLE IF NOT EXISTS public.file_info
(
    file_id serial NOT NULL,
    "timestamp" timestamp with time zone,
    file_name text COLLATE pg_catalog."default",
    user_id smallint,
    url text COLLATE pg_catalog."default",
    album_id smallint,
    CONSTRAINT file_info_pkey PRIMARY KEY (file_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.file_info
    OWNER to postgres;