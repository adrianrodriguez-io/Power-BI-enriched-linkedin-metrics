-- Table: public.posts

-- DROP TABLE IF EXISTS public.posts;

CREATE TABLE IF NOT EXISTS public.posts
(
    id integer NOT NULL DEFAULT nextval('posts_id_seq'::regclass),
    idpost bigint NOT NULL,
    url character varying(300) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    text text COLLATE pg_catalog."default",
    datetime timestamp without time zone DEFAULT now(),
    CONSTRAINT posts_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.posts
    OWNER to postgres;
	
	
-- Table: public.metrics

-- DROP TABLE IF EXISTS public.metrics;

CREATE TABLE IF NOT EXISTS public.metrics
(
    id integer NOT NULL DEFAULT nextval('metrics_id_seq'::regclass),
    idpost bigint NOT NULL,
    datetime timestamp without time zone NOT NULL DEFAULT now(),
    impressions integer NOT NULL,
    likes integer,
    comments integer,
    shares integer
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.metrics
    OWNER to postgres;
	
-- Table: public.executionlogs

-- DROP TABLE IF EXISTS public.executionlogs;

CREATE TABLE IF NOT EXISTS public.executionlogs
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    idexec bigint,
    startdatetime timestamp without time zone,
    finisheddatetime timestamp without time zone,
    exectype character varying(50) COLLATE pg_catalog."default",
    execstatus character varying(50) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.executionlogs
    OWNER to postgres;
