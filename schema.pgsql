--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: player; Type: TABLE; Schema: public; Owner: csmeteo; Tablespace: 
--

CREATE TABLE player (
    id integer NOT NULL,
    name character varying(100),
    kills integer DEFAULT 0,
    map character varying(30),
    "time" double precision,
    realtime double precision,
    temperature character varying(100),
    condition character varying(100),
    humidity character varying(100),
    pressure character varying(100)
);


ALTER TABLE public.player OWNER TO csmeteo;

--
-- Name: player_id_seq; Type: SEQUENCE; Schema: public; Owner: csmeteo
--

CREATE SEQUENCE player_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.player_id_seq OWNER TO csmeteo;

--
-- Name: player_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: csmeteo
--

ALTER SEQUENCE player_id_seq OWNED BY player.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: csmeteo
--

ALTER TABLE player ALTER COLUMN id SET DEFAULT nextval('player_id_seq'::regclass);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

