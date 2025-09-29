--
-- PostgreSQL database dump
--

\restrict 6TasQfwPkxgYfLNeoehO5oXOwPrD5nTDaoZZDeVaQZXBpz1vVpqdlbWQUXREWz7

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

-- Started on 2025-09-28 20:08:51

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 16389)
-- Name: categorias_reciclaje; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categorias_reciclaje (
    id_categoria integer NOT NULL,
    nombre_categoria character varying,
    descripcion character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.categorias_reciclaje OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 24576)
-- Name: materialxcentro; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.materialxcentro
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 1000
    CACHE 1
    CYCLE;


ALTER SEQUENCE public.materialxcentro OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16417)
-- Name: centros_materiales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.centros_materiales (
    id_centro_material integer DEFAULT nextval('public.materialxcentro'::regclass) NOT NULL,
    id_centro integer,
    id_material integer,
    created_at timestamp without time zone
);


ALTER TABLE public.centros_materiales OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16410)
-- Name: centros_reciclaje; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.centros_reciclaje (
    id_centro integer NOT NULL,
    nombre_centro character varying,
    direccion character varying,
    telefono character varying,
    horario_atencion character varying,
    latitud numeric,
    longitud numeric,
    created_at timestamp without time zone
);


ALTER TABLE public.centros_reciclaje OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16443)
-- Name: consejos_ecologicos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.consejos_ecologicos (
    id_consejo integer NOT NULL,
    titulo character varying,
    contenido character varying,
    imagen_url character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.consejos_ecologicos OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16403)
-- Name: instrucciones_reciclaje; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.instrucciones_reciclaje (
    id_instruccion integer NOT NULL,
    id_material integer,
    paso_numero integer,
    instruccion text,
    imagen_url character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.instrucciones_reciclaje OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 24579)
-- Name: noticias_reciclaje; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.noticias_reciclaje (
    id_noticia integer NOT NULL,
    titulo character varying(200) NOT NULL,
    resumen text,
    contenido text,
    fecha_publicacion date,
    fuente character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.noticias_reciclaje OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 24578)
-- Name: noticias_reciclaje_id_noticia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.noticias_reciclaje_id_noticia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.noticias_reciclaje_id_noticia_seq OWNER TO postgres;

--
-- TOC entry 4968 (class 0 OID 0)
-- Dependencies: 227
-- Name: noticias_reciclaje_id_noticia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.noticias_reciclaje_id_noticia_seq OWNED BY public.noticias_reciclaje.id_noticia;


--
-- TOC entry 224 (class 1259 OID 16436)
-- Name: preguntas_frecuentes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.preguntas_frecuentes (
    id_pregunta integer NOT NULL,
    pregunta character varying,
    respuesta character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.preguntas_frecuentes OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 24589)
-- Name: recordatorios_reciclaje; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recordatorios_reciclaje (
    id_recordatorio integer NOT NULL,
    titulo character varying(100) NOT NULL,
    descripcion text,
    fecha_recordatorio date NOT NULL,
    hora_recordatorio time without time zone NOT NULL,
    repetir_semanal boolean DEFAULT false,
    activo boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.recordatorios_reciclaje OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 24588)
-- Name: recordatorios_reciclaje_id_recordatorio_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.recordatorios_reciclaje_id_recordatorio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recordatorios_reciclaje_id_recordatorio_seq OWNER TO postgres;

--
-- TOC entry 4969 (class 0 OID 0)
-- Dependencies: 229
-- Name: recordatorios_reciclaje_id_recordatorio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.recordatorios_reciclaje_id_recordatorio_seq OWNED BY public.recordatorios_reciclaje.id_recordatorio;


--
-- TOC entry 218 (class 1259 OID 16396)
-- Name: tipos_material; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipos_material (
    id_material integer NOT NULL,
    id_categoria integer,
    nombre_material character varying,
    descripcion character varying,
    tiempo_descomposicion character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.tipos_material OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16429)
-- Name: user_logros; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_logros (
    id_logro integer NOT NULL,
    id_usuario integer,
    tipo_logro character varying,
    fecha_obtencion timestamp without time zone
);


ALTER TABLE public.user_logros OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16422)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    nombre character varying,
    email character varying,
    password_hash character varying,
    localidad character varying,
    created_at timestamp without time zone
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 4785 (class 2604 OID 24582)
-- Name: noticias_reciclaje id_noticia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.noticias_reciclaje ALTER COLUMN id_noticia SET DEFAULT nextval('public.noticias_reciclaje_id_noticia_seq'::regclass);


--
-- TOC entry 4787 (class 2604 OID 24592)
-- Name: recordatorios_reciclaje id_recordatorio; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recordatorios_reciclaje ALTER COLUMN id_recordatorio SET DEFAULT nextval('public.recordatorios_reciclaje_id_recordatorio_seq'::regclass);


--
-- TOC entry 4792 (class 2606 OID 16395)
-- Name: categorias_reciclaje categorias_reciclaje_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias_reciclaje
    ADD CONSTRAINT categorias_reciclaje_pkey PRIMARY KEY (id_categoria);


--
-- TOC entry 4800 (class 2606 OID 16421)
-- Name: centros_materiales centros_materiales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centros_materiales
    ADD CONSTRAINT centros_materiales_pkey PRIMARY KEY (id_centro_material);


--
-- TOC entry 4798 (class 2606 OID 16416)
-- Name: centros_reciclaje centros_reciclaje_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centros_reciclaje
    ADD CONSTRAINT centros_reciclaje_pkey PRIMARY KEY (id_centro);


--
-- TOC entry 4808 (class 2606 OID 16449)
-- Name: consejos_ecologicos consejos_ecologicos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consejos_ecologicos
    ADD CONSTRAINT consejos_ecologicos_pkey PRIMARY KEY (id_consejo);


--
-- TOC entry 4796 (class 2606 OID 16409)
-- Name: instrucciones_reciclaje instrucciones_reciclaje_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instrucciones_reciclaje
    ADD CONSTRAINT instrucciones_reciclaje_pkey PRIMARY KEY (id_instruccion);


--
-- TOC entry 4810 (class 2606 OID 24587)
-- Name: noticias_reciclaje noticias_reciclaje_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.noticias_reciclaje
    ADD CONSTRAINT noticias_reciclaje_pkey PRIMARY KEY (id_noticia);


--
-- TOC entry 4806 (class 2606 OID 16442)
-- Name: preguntas_frecuentes preguntas_frecuentes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.preguntas_frecuentes
    ADD CONSTRAINT preguntas_frecuentes_pkey PRIMARY KEY (id_pregunta);


--
-- TOC entry 4812 (class 2606 OID 24599)
-- Name: recordatorios_reciclaje recordatorios_reciclaje_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recordatorios_reciclaje
    ADD CONSTRAINT recordatorios_reciclaje_pkey PRIMARY KEY (id_recordatorio);


--
-- TOC entry 4794 (class 2606 OID 16402)
-- Name: tipos_material tipos_material_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_material
    ADD CONSTRAINT tipos_material_pkey PRIMARY KEY (id_material);


--
-- TOC entry 4804 (class 2606 OID 16435)
-- Name: user_logros user_logros_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_logros
    ADD CONSTRAINT user_logros_pkey PRIMARY KEY (id_logro);


--
-- TOC entry 4802 (class 2606 OID 16428)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);


--
-- TOC entry 4815 (class 2606 OID 16455)
-- Name: centros_materiales centros_materiales_id_centro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centros_materiales
    ADD CONSTRAINT centros_materiales_id_centro_fkey FOREIGN KEY (id_centro) REFERENCES public.centros_reciclaje(id_centro);


--
-- TOC entry 4816 (class 2606 OID 16460)
-- Name: centros_materiales centros_materiales_id_material_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.centros_materiales
    ADD CONSTRAINT centros_materiales_id_material_fkey FOREIGN KEY (id_material) REFERENCES public.tipos_material(id_material);


--
-- TOC entry 4814 (class 2606 OID 16470)
-- Name: instrucciones_reciclaje instrucciones_reciclaje_id_material_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instrucciones_reciclaje
    ADD CONSTRAINT instrucciones_reciclaje_id_material_fkey FOREIGN KEY (id_material) REFERENCES public.tipos_material(id_material);


--
-- TOC entry 4813 (class 2606 OID 16465)
-- Name: tipos_material tipos_material_id_categoria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_material
    ADD CONSTRAINT tipos_material_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES public.categorias_reciclaje(id_categoria);


--
-- TOC entry 4817 (class 2606 OID 16450)
-- Name: user_logros user_logros_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_logros
    ADD CONSTRAINT user_logros_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);


-- Completed on 2025-09-28 20:08:52

--
-- PostgreSQL database dump complete
--

\unrestrict 6TasQfwPkxgYfLNeoehO5oXOwPrD5nTDaoZZDeVaQZXBpz1vVpqdlbWQUXREWz7

