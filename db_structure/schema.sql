--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.7
-- Dumped by pg_dump version 9.4.1
-- Started on 2015-05-29 10:45:41 NOVT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 179 (class 3079 OID 11759)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2002 (class 0 OID 0)
-- Dependencies: 179
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 170 (class 1259 OID 19346)
-- Name: email_mailru; Type: TABLE; Schema: public; Owner: web_script; Tablespace: 
--

CREATE TABLE email_mailru (
    id integer NOT NULL,
    email character varying(120),
    domain character varying(40),
    password character varying(60),
    fio character varying(240),
    birthday character varying(60),
    male boolean,
    created timestamp without time zone DEFAULT now(),
    active boolean DEFAULT false,
    error_counter integer DEFAULT 0
);


ALTER TABLE email_mailru OWNER TO web_script;

--
-- TOC entry 2003 (class 0 OID 0)
-- Dependencies: 170
-- Name: TABLE email_mailru; Type: COMMENT; Schema: public; Owner: web_script
--

COMMENT ON TABLE email_mailru IS 'Проект "Регистратор". Таблица аккаунтов на Mail.ru';


--
-- TOC entry 171 (class 1259 OID 19349)
-- Name: email_mailru_id_seq; Type: SEQUENCE; Schema: public; Owner: web_script
--

CREATE SEQUENCE email_mailru_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE email_mailru_id_seq OWNER TO web_script;

--
-- TOC entry 2004 (class 0 OID 0)
-- Dependencies: 171
-- Name: email_mailru_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: web_script
--

ALTER SEQUENCE email_mailru_id_seq OWNED BY email_mailru.id;


--
-- TOC entry 172 (class 1259 OID 19361)
-- Name: family_name; Type: TABLE; Schema: public; Owner: web_script; Tablespace: 
--

CREATE TABLE family_name (
    name character varying(120) NOT NULL,
    male boolean
);


ALTER TABLE family_name OWNER TO web_script;

--
-- TOC entry 2005 (class 0 OID 0)
-- Dependencies: 172
-- Name: TABLE family_name; Type: COMMENT; Schema: public; Owner: web_script
--

COMMENT ON TABLE family_name IS 'Проект "Виртуальные-люди". Таблица фамилий.';


--
-- TOC entry 173 (class 1259 OID 19366)
-- Name: first_name; Type: TABLE; Schema: public; Owner: web_script; Tablespace: 
--

CREATE TABLE first_name (
    name character varying(120) NOT NULL,
    male boolean
);


ALTER TABLE first_name OWNER TO web_script;

--
-- TOC entry 2006 (class 0 OID 0)
-- Dependencies: 173
-- Name: TABLE first_name; Type: COMMENT; Schema: public; Owner: web_script
--

COMMENT ON TABLE first_name IS 'Проект "Виртуальные-люди". Таблица имен.';


--
-- TOC entry 177 (class 1259 OID 19417)
-- Name: fotostrana_accounts; Type: TABLE; Schema: public; Owner: web_script; Tablespace: 
--

CREATE TABLE fotostrana_accounts (
    email_id integer NOT NULL,
    email_send boolean DEFAULT false,
    email_activated boolean DEFAULT false
);


ALTER TABLE fotostrana_accounts OWNER TO web_script;

--
-- TOC entry 2007 (class 0 OID 0)
-- Dependencies: 177
-- Name: TABLE fotostrana_accounts; Type: COMMENT; Schema: public; Owner: web_script
--

COMMENT ON TABLE fotostrana_accounts IS 'Проект "Регистратор". Таблица аккаунтов на Фотостране (Привязка к Email)';


--
-- TOC entry 175 (class 1259 OID 19376)
-- Name: https_proxy; Type: TABLE; Schema: public; Owner: web_script; Tablespace: 
--

CREATE TABLE https_proxy (
    ip_address character varying(48) NOT NULL,
    port integer NOT NULL,
    active boolean DEFAULT true,
    good boolean DEFAULT false,
    add_date timestamp without time zone DEFAULT now()
);


ALTER TABLE https_proxy OWNER TO web_script;

--
-- TOC entry 2008 (class 0 OID 0)
-- Dependencies: 175
-- Name: TABLE https_proxy; Type: COMMENT; Schema: public; Owner: web_script
--

COMMENT ON TABLE https_proxy IS 'Проект "Прокси". Таблица прокси-серверов с поддержкой HTTPS';


--
-- TOC entry 174 (class 1259 OID 19371)
-- Name: last_name; Type: TABLE; Schema: public; Owner: web_script; Tablespace: 
--

CREATE TABLE last_name (
    name character varying(120) NOT NULL,
    male boolean NOT NULL
);


ALTER TABLE last_name OWNER TO web_script;

--
-- TOC entry 2009 (class 0 OID 0)
-- Dependencies: 174
-- Name: TABLE last_name; Type: COMMENT; Schema: public; Owner: web_script
--

COMMENT ON TABLE last_name IS 'Проект "Виртуальные-люди". Таблица отчеств.';


--
-- TOC entry 178 (class 1259 OID 19426)
-- Name: livejournal_accounts; Type: TABLE; Schema: public; Owner: web_script; Tablespace: 
--

CREATE TABLE livejournal_accounts (
    email_id integer NOT NULL,
    email_send boolean DEFAULT false,
    email_activated boolean DEFAULT false,
    error_counter integer DEFAULT 0,
    password character varying(120),
    login character varying(120)
);


ALTER TABLE livejournal_accounts OWNER TO web_script;

--
-- TOC entry 2010 (class 0 OID 0)
-- Dependencies: 178
-- Name: TABLE livejournal_accounts; Type: COMMENT; Schema: public; Owner: web_script
--

COMMENT ON TABLE livejournal_accounts IS 'Проект "Регистратор". Таблица аккаунтов на LiveJournal (Привязка к Email)';


--
-- TOC entry 176 (class 1259 OID 19384)
-- Name: random_https_proxy; Type: VIEW; Schema: public; Owner: web_script
--

CREATE VIEW random_https_proxy AS
 SELECT https_proxy.ip_address,
    https_proxy.port
   FROM https_proxy
  WHERE ((https_proxy.active = true) AND (https_proxy.good = true))
  ORDER BY random()
 LIMIT 1;


ALTER TABLE random_https_proxy OWNER TO web_script;

--
-- TOC entry 1860 (class 2604 OID 19351)
-- Name: id; Type: DEFAULT; Schema: public; Owner: web_script
--

ALTER TABLE ONLY email_mailru ALTER COLUMN id SET DEFAULT nextval('email_mailru_id_seq'::regclass);


--
-- TOC entry 1874 (class 2606 OID 19359)
-- Name: email_mailru_pkey; Type: CONSTRAINT; Schema: public; Owner: web_script; Tablespace: 
--

ALTER TABLE ONLY email_mailru
    ADD CONSTRAINT email_mailru_pkey PRIMARY KEY (id);


--
-- TOC entry 1876 (class 2606 OID 19365)
-- Name: family_name_pkey; Type: CONSTRAINT; Schema: public; Owner: web_script; Tablespace: 
--

ALTER TABLE ONLY family_name
    ADD CONSTRAINT family_name_pkey PRIMARY KEY (name);


--
-- TOC entry 1878 (class 2606 OID 19370)
-- Name: first_name_pkey; Type: CONSTRAINT; Schema: public; Owner: web_script; Tablespace: 
--

ALTER TABLE ONLY first_name
    ADD CONSTRAINT first_name_pkey PRIMARY KEY (name);


--
-- TOC entry 1884 (class 2606 OID 19421)
-- Name: fotostrana_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: web_script; Tablespace: 
--

ALTER TABLE ONLY fotostrana_accounts
    ADD CONSTRAINT fotostrana_accounts_pkey PRIMARY KEY (email_id);


--
-- TOC entry 1882 (class 2606 OID 19383)
-- Name: https_pkey; Type: CONSTRAINT; Schema: public; Owner: web_script; Tablespace: 
--

ALTER TABLE ONLY https_proxy
    ADD CONSTRAINT https_pkey PRIMARY KEY (ip_address, port);


--
-- TOC entry 1880 (class 2606 OID 19375)
-- Name: last_name_pkey; Type: CONSTRAINT; Schema: public; Owner: web_script; Tablespace: 
--

ALTER TABLE ONLY last_name
    ADD CONSTRAINT last_name_pkey PRIMARY KEY (name);


--
-- TOC entry 1886 (class 2606 OID 19430)
-- Name: livejournal_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: web_script; Tablespace: 
--

ALTER TABLE ONLY livejournal_accounts
    ADD CONSTRAINT livejournal_accounts_pkey PRIMARY KEY (email_id);


--
-- TOC entry 1872 (class 1259 OID 19360)
-- Name: email_mailru_email_domain_idx; Type: INDEX; Schema: public; Owner: web_script; Tablespace: 
--

CREATE UNIQUE INDEX email_mailru_email_domain_idx ON email_mailru USING btree (email, domain);


--
-- TOC entry 2001 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2015-05-29 10:46:14 NOVT

--
-- PostgreSQL database dump complete
--

